from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db import transaction
from .models.chat_session import ChatSession
from .models.chat_message import ChatMessage
from rest_framework import viewsets
from django.db.models import Subquery, OuterRef

from inventory.models import Product
from .models import ChatSession, ChatMessage  # Importamos los nuevos modelos
import requests
import json
from dotenv import load_dotenv
import os
import logging

# Cargar variables de entorno
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI-API-KEY')

# Configuración de endpoints de IA
OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"

logger = logging.getLogger(__name__)

def get_openai_response(messages, temperature=0.3, model="gpt-4o-mini"):
    """Obtiene respuesta de la API de OpenAI con seguridad mejorada"""
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
    """Obtiene opciones de filtrado disponibles desde la base de datos"""
    categories = Product.objects.values_list('category', flat=True).distinct()
    brands = Product.objects.values_list('brand', flat=True).distinct()
    return str(categories), str(brands)

def generate_query_agent(prompt, chat_history):
    """Genera consultas de base de datos usando IA con contexto histórico"""
    categories, brands = get_possible_filter_options()
    
    system_prompt = f"""Eres un experto en Django ORM. Instrucciones:
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
    """Genera respuestas naturales basadas en resultados de productos"""
    processed_results = []
    for item in results:
        processed_item = item.copy()
        if 'price' in processed_item:
            processed_item['price'] = float(processed_item['price'])
        processed_results.append(processed_item)

    system_prompt = f"""Analiza estos resultados y genera una respuesta natural:

    - Destaca características clave
    - Menciona disponibilidad
    - Precios relevantes
    - Mantén respuestas concisas
    - Trata de animar al usuario a comprar el articulo o seguir explorando
    - Pregunta: {question}
    - Resultados: {json.dumps(processed_results[:3]) if len(processed_results) > 3 else processed_results}
    """
    
    return get_openai_response([{"role": "system", "content": system_prompt}])

class ChatBotViewSet(viewsets.ViewSet):
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

class ChatBotView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            user_message = data.get('message')
            session_id = data.get('session_id')
            
            # Manejar usuario anónimo o autenticado
            user = request.user if request.user.is_authenticated else None

            logger.info(f"Procesando mensaje: {user_message} para sesión: {session_id}")

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

            # Guardar mensaje del usuario
            user_message_obj = ChatMessage.objects.create(
                session=chat_session,
                message_text=user_message,
                is_bot=False
            )
            logger.info(f"Mensaje de usuario guardado: {user_message_obj.id}")

            # Generar respuesta del bot
            history_chat = get_chat_history(chat_session.id)
            bot_response = self.generate_bot_response(user_message,history_chat)

            # Guardar respuesta del bot
            bot_message = ChatMessage.objects.create(
                session=chat_session,
                message_text=bot_response,
                is_bot=True
            )
            logger.info(f"Respuesta del bot guardada: {bot_message.id}")

            return Response({
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
                }
            }, status=status.HTTP_200_OK)

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



class ChatBotView(APIView):
    """ Uncomment this code for JWT and user validation
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Opcional: permite anónimos si lo necesitas
    """
    def post(self, request):
        """Maneja la lógica principal del chatbot con persistencia en DB"""
        try:
            data = json.loads(request.body)
            user_message = data['message']
            
            # 1. Manejo de sesiones
            session, created = ChatSession.objects.get_or_create(
                id=request.data.get('session_id'),  # Si viene de frontend
                defaults={
                    'user': request.user if request.user.is_authenticated else None
                }
            )
            
            # 2. Recuperar historial desde DB en lugar de caché
            chat_history = ChatMessage.objects.filter(
                session=session
            ).order_by('created_at')[:10]  # Últimos 10 mensajes
            
            # 3. Formatear historial para los agentes de IA
            formatted_history = []
            for msg in chat_history:
                role = "assistant" if msg.is_bot else "user"
                formatted_history.append({"role": role, "content": msg.message_text})
            
            # 4. Generar consulta de productos
            generated_query = generate_query_agent(user_message, formatted_history)
            
            # 5. Ejecutar consulta de forma segura
            safe_globals = {'Product': Product}
            try:
                products = eval(generated_query, {"__builtins__": None}, safe_globals)
                results = list(products.values('name', 'brand', 'price', 'stock', 'features'))
            except Exception as e:
                results = []
                error_message = f"Error en consulta: {str(e)}"
                ChatMessage.objects.create(
                    session=session,
                    message_text=error_message,
                    is_bot=True
                )
                return JsonResponse({"error": error_message}, status=400)
            
            # 6. Generar respuesta natural
            bot_response = generate_response_agent(results, user_message)
            
            # 7. Guardar en base de datos (ambos mensajes)
            ChatMessage.objects.bulk_create([
                ChatMessage(
                    session=session,
                    message_text=user_message,
                    is_bot=False
                ),
                ChatMessage(
                    session=session,
                    message_text=bot_response,
                    is_bot=True,
                    product=products.first() if results else None  # Vincular producto si existe
                )
            ])
            
            return JsonResponse({
                "response": bot_response,
                "results_count": len(results),
                "session_id": str(session.id)  # Importante para continuar la conversación
            })
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        except KeyError:
            return JsonResponse({"error": "Campo 'message' requerido"}, status=400)
        except Exception as e:
            ChatMessage.objects.create(
                session=session,
                message_text=f"Error crítico: {str(e)}",
                is_bot=True
            )
            return JsonResponse({"error": str(e)}, status=500)

    def get(self, request):
        """Obtiene información de sesión activa"""
        session_id = request.query_params.get('session_id')
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id)
                messages = ChatMessage.objects.filter(session=session)
                return JsonResponse({
                    "session_id": str(session.id),
                    "messages": [{
                        "text": msg.message_text,
                        "is_bot": msg.is_bot,
                        "timestamp": msg.created_at
                    } for msg in messages]
                })
            except ChatSession.DoesNotExist:
                return JsonResponse({"error": "Sesión no encontrada"}, status=404)
        return JsonResponse({"message": "Proporciona session_id para recuperar historial"}, status=400)
