from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db import transaction
from .models.chat_session import ChatSession
from .models.chat_message import ChatMessage
from rest_framework import viewsets
from django.db.models import Subquery, OuterRef
from decimal import Decimal

from inventory.models import Product
from recomendations.models import Recommendation

import requests
import json
from dotenv import load_dotenv
import os
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"


load_dotenv()  # carga las variables del .env

## DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI-API-KEY')

DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

logger = logging.getLogger(__name__)

def get_openai_response(messages, temperature=0.3, model="gpt-4o-mini"):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    
    response = requests.post(OPENAI_ENDPOINT, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

def get_chat_history(session_id):
    formatted_history = []
    chat_history = ChatMessage.objects.filter(session_id=session_id).order_by('created_at')[:10]
    for msg in chat_history:
        role = "assistant" if msg.is_bot else "user"
        formatted_history.append({"role": role, "content": msg.message_text})
    return formatted_history

def get_possible_filter_options():
    qcat = Product.objects.values('category').distinct()
    qbrand = Product.objects.values('brand').distinct()

    return [str(qcat), str(qbrand)]

# Modificaciones en los agentes (solo cambia la función de llamada)
def generate_query_agent(prompt, chat_history):
    possible_filter_options = get_possible_filter_options()
    system_prompt = f"""Eres un experto en Django ORM. Genera consultas de base de datos basadas en:
    1. Campos disponibles: name, brand, category, price, stock, features (JSON)
    2. Para features usar sintaxis de doble guión: features__ram=16GB
    3. Solo devuelve el código Python/Django ORM, sin explicaciones y tampoco tags de descripción de código
    4. Ejemplos válidos:
       - Product.objects.filter(category='Laptops', stock__gt=0)
       - Product.objects.filter(features__storage__icontains='512GB').exclude(stock=0)
       - ¡INCORRECTO! Product.objects.filter(category='Laptops').count()
    5. CRUCIAL: Solo usa métodos que devuelvan registros (filter/get/exclude/order_by). Prohibido count/aggregate/annotate/values
    6. Ten en cuenta que hay estas opciones de categoria {possible_filter_options[0]} y de marca {possible_filter_options[1]}
    7. Ten en cuenta que el usuario tiene un historial de preguntas y respuestas {chat_history}
    
    
    Pregunta del usuario: {prompt}
    """
    print(system_prompt)
    return get_openai_response([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ])

def generate_response_agent(results, question):
    # Convertir Decimal a float en los resultados
    processed_results = []
    for item in results:
        processed_item = item.copy()
        if 'price' in processed_item:
            processed_item['price'] = float(processed_item['price'])
        processed_results.append(processed_item)

    system_prompt = f"""Analiza estos resultados de productos y genera una respuesta natural:
    - Destaca características clave
    - Menciona disponibilidad
    - Precios relevantes
    - Mantén respuestas concisas
    
    Pregunta original: {question}
    """

    if len(processed_results) < 3:
        system_prompt += f"""
        Resultados: {json.dumps(processed_results)}
        """
    else:
        system_prompt += f"""
        Resultados: {json.dumps(processed_results[:3])} (mostrando primeros 3 de {len(processed_results)})
        """
    
    return get_openai_response([{
        "role": "system",
        "content": system_prompt
    }])

def generate_recommendations_query(user_history, chat_history):
    try:
        # Extraer las categorías y marcas más frecuentes del historial
        preferred_categories = list(set([h['product__category'] for h in user_history if h['product__category']]))
        preferred_brands = list(set([h['product__brand'] for h in user_history if h['product__brand']]))
        
        # Construir la query directamente en lugar de usar OpenAI
        if preferred_categories and preferred_brands:
            query = """
            Product.objects.filter(
                recommendation__user=user,
                stock__gt=0
            ).filter(
                category__in=preferred_categories
            ).order_by('-recommendation__score', '-recommendation__created_at').distinct()[:5]
            """
        else:
            query = """
            Product.objects.filter(
                recommendation__user=user,
                stock__gt=0
            ).order_by('-recommendation__score', '-recommendation__created_at').distinct()[:5]
            """

        logger.info(f"Query de recomendaciones generada: {query}")
        return query.strip()

    except Exception as e:
        logger.error(f"Error generando query de recomendaciones: {str(e)}")
        return """
        Product.objects.filter(
            recommendation__user=user,
            stock__gt=0
        ).order_by('-recommendation__score').distinct()[:5]
        """

def get_user_recommendations(request, user_message, session_id=None):
    try:
        user = request.user if request.user.is_authenticated else None
        if not user:
            print("No hay usuario autenticado")
            return []

        # Obtener historial de recomendaciones
        user_history = Recommendation.objects.filter(user=user)

        # Consulta directa con clasificación
        all_products = Product.objects.filter(
            recommendation__user=user,
            stock__gt=0
        ).order_by('-recommendation__score', '-recommendation__created_at').distinct()

        # Inicializar lista para los productos
        products_data = []
        for product in all_products:
            recommendation = Recommendation.objects.filter(user=user, product=product).first()
            score = recommendation.score if recommendation else 0
            
            product_data = {
                'name': product.name,
                'brand': product.brand,
                'price': float(product.price) if isinstance(product.price, Decimal) else product.price,
                'stock': product.stock,
                'features': product.features,
                'score': score
            }
            products_data.append(product_data)

        # Ordenar los productos por score
        products_data.sort(key=lambda x: x['score'])

        # Seleccionar el mejor, el del medio y el peor producto
        best_product = products_data[-1] if len(products_data) > 0 else None  # Mejor producto
        average_product = products_data[len(products_data) // 2] if len(products_data) > 1 else None  # Producto del medio
        worst_product = products_data[0] if len(products_data) > 0 else None  # Peor producto

        # Crear una lista de recomendaciones
        recommendations = []
        if best_product:
            recommendations.append(best_product)
        if average_product:
            recommendations.append(average_product)
        if worst_product:
            recommendations.append(worst_product)

        print("\n=== Productos Clasificados ===")
        print(f"Mejor Producto: {best_product}")
        print(f"Producto del Medio: {average_product}")
        print(f"Peor Producto: {worst_product}")

        return recommendations

    except Exception as e:
        print(f"\n=== Error en Recomendaciones ===")
        print(f"Error: {str(e)}")
        logger.error(f"Error en recomendaciones: {str(e)}")
        return []

class ChatBotViewSet(viewsets.ViewSet):
    # Obtener conversaciones del usuario
    def get_conversations(self, request):
        try:
            user = request.user if request.user.is_authenticated else None
            
            conversations = ChatSession.objects.filter(
                user=user
            ).annotate(
                last_message=Subquery(
                    ChatMessage.objects.filter(
                        session=OuterRef('pk')
                    ).order_by('-created_at').values('message_text')[:1]
                )
            ).order_by('-created_at')[:10]

            return Response({
                'conversations': [{
                    'id': str(conv.id),
                    'created_at': conv.created_at,
                    'last_message': conv.last_message,
                } for conv in conversations]
            })
        except Exception as e:
            logger.error(f"Error obteniendo conversaciones: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_messages(self, request, conversation_id):
        try:
            messages = ChatMessage.objects.filter(
                session_id=conversation_id
            ).order_by('created_at')

            return Response({
                'messages': [{
                    'id': msg.id,
                    'message_text': msg.message_text,
                    'is_bot': msg.is_bot,
                    'created_at': msg.created_at
                } for msg in messages]
            })
        except Exception as e:
            logger.error(f"Error obteniendo mensajes: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BaseChatView(APIView):
    def get_user(self, request):
        return request.user if request.user.is_authenticated else None

class ChatHistoryView(BaseChatView):
    def get(self, request):
        user = self.get_user(request)
        if not user:
            return Response({"error": "No authenticated user"}, status=status.HTTP_401_UNAUTHORIZED)
        # Lógica para obtener el historial de chat
        return Response({"history": "Chat history data"})

class SendMessageView(BaseChatView):
    def post(self, request):
        user = self.get_user(request)
        if not user:
            return Response({"error": "No authenticated user"}, status=status.HTTP_401_UNAUTHORIZED)
        # Lógica para enviar un mensaje
        return Response({"message": "Message sent"}, status=status.HTTP_200_OK)

class ChatBotView(APIView):
    authentication_classes = [JWTAuthentication]
    # Si quieres que la autenticación sea opcional, no incluyas permission_classes
    # Si quieres que sea obligatoria, descomenta la siguiente línea:
    # permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            user_message = data.get('message')
            session_id = data.get('session_id')
            
            # Obtener el usuario autenticado
            user = request.user if request.user.is_authenticated else None
            logger.info(f"Usuario autenticado: {user}")
            
            print(user_message)
            print(session_id)
            
            print(f"Procesando mensaje: {user_message} para sesión: {session_id}")

            # Validar mensaje
            if not user_message:
                return Response({"error": "El mensaje es requerido"}, status=status.HTTP_400_BAD_REQUEST)

            # Gestionar sesión
            if session_id:
                try:
                    chat_session = ChatSession.objects.get(id=session_id)
                except ChatSession.DoesNotExist:
                    chat_session = ChatSession.objects.create(user=user)
                    logger.info(f"Nueva sesión creada: {chat_session.id}")
            else:
                chat_session = ChatSession.objects.create(user=user)
                logger.info(f"Nueva sesión creada: {chat_session.id}")

            # Generar respuesta del bot
            history_chat = get_chat_history(chat_session.id)
            generated_query = generate_query_agent(user_message, history_chat)
            products = eval(generated_query, {"__builtins__": None}, {'Product': Product})
            results = list(products.values('name', 'brand', 'price', 'stock', 'features'))
            


            # Guardar recomendaciones solo si el usuario está autenticado
            if user and user.is_authenticated:
                for product in products:
                    # Determinar categoría y score basado en stock y precio
                    if product.stock > 10 and product.price < Decimal('1000'):
                        category = 'Altamente Recomendado'
                        score = Decimal('0.95')
                    elif product.stock > 0:
                        category = 'Recomendado'
                        score = Decimal('0.75')
                    else:
                        category = 'No Recomendado'
                        score = Decimal('0.50')

                    # Crear o actualizar recomendación
                    Recommendation.objects.update_or_create(
                        user=user,
                        product=product,
                        defaults={
                            'score': score,
                            'category': category
                        }
                    )
                    print(f"Recomendación guardada: {product.name} para {user.username}")
                    logger.info(f"Guardando recomendación para usuario: {user.username}")

            bot_response = generate_response_agent(results, user_message)

            # Guardar mensajes
            user_message_obj = ChatMessage.objects.create(
                session=chat_session,
                message_text=user_message,
                is_bot=False
            )

            bot_message = ChatMessage.objects.create(
                session=chat_session,
                message_text=bot_response,
                is_bot=True
            )

            # Obtener recomendaciones personalizadas
            recommended_products = get_user_recommendations(request, user_message, session_id)

            # Incluir recomendaciones en la respuesta
            response_data = {
                "session_id": str(chat_session.id),
                "messages": {
                    "user_message": {
                        "id": user_message_obj.id,
                        "text": user_message_obj.message_text,
                        "created_at": user_message_obj.created_at
                    },
                    "bot_message": {
                        "id": bot_message.id,
                        "text": bot_message.message_text,
                        "created_at": bot_message.created_at
                    }
                },
                "recommendations": recommended_products if recommended_products else []
            }
            
            print(response_data)
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error en el procesamiento del chat: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            session_id = request.GET.get('session_id')
            
            if not session_id:
                return Response({"error": "Se requiere session_id"}, status=status.HTTP_400_BAD_REQUEST)
                
            # Obtener mensajes de la sesión
            messages = ChatMessage.objects.filter(
                session_id=session_id
            ).order_by('created_at').values(
                'id',
                'message_text',
                'is_bot',
                'created_at'
            )
            
            return Response({
                "session_id": session_id,
                "messages": list(messages)
            })
            
        except Exception as e:
            logger.error(f"Error obteniendo historial: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def generate_bot_response(self, user_message, history_chat):
        # Aquí va tu lógica existente de generación de respuesta
        # Usando generate_query_agent y generate_response_agent
        try:
            generated_query = generate_query_agent(user_message, history_chat)
            products = eval(generated_query, {"__builtins__": None}, {'Product': Product})
            results = list(products.values('name', 'brand', 'price', 'stock', 'features'))
            bot_response = generate_response_agent(results, user_message)
            return bot_response
        except Exception as e:
            logger.error(f"Error generando respuesta del bot: {str(e)}")
            return "Lo siento, hubo un error procesando tu mensaje."
