 
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from inventory.models import Product

import requests
import json
from dotenv import load_dotenv
import os


OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"


load_dotenv()  # carga las variables del .env

## DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI-API-KEY')

DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

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
    6. Ten en  cuenta que hay estas opciones de categoria {possible_filter_options[0]} y de marca {possible_filter_options[1]}
    
    
    Pregunta del usuario: {prompt}
    Historial: {chat_history}
    """
    
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




class ChatBotView(APIView):
    def post(self, request):        
        data = json.loads(request.body)
        user_message = data['message']
        session_key = request.session.session_key
        
        # Recuperar historial de caché
        cache_key = f"chat_history_{session_key}"
        chat_history = cache.get(cache_key, [])

        generated_query = generate_query_agent(user_message, chat_history[-2:])
        print(generated_query)
        
       
        # Generar consulta con contexto histórico
        
        
        # Ejecutar consulta de forma segura
        safe_globals = {'Product': Product}
        products = eval(generated_query, {"__builtins__": None}, safe_globals)
        results = list(products.values('name', 'brand', 'price', 'stock', 'features'))

        print(results)
        
        # Generar respuesta natural
        bot_response = generate_response_agent(results, user_message)
        
        # Actualizar caché y historial
        chat_history.append({"user": user_message, "bot": bot_response})

        try:
            cache.set(cache_key, chat_history, timeout=3600)  # 1 hora de caché
            
            return JsonResponse({"response": bot_response, "results_count": len(results)})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request):
        # Opcional: Puedes añadir esto si quieres manejar solicitudes GET
        return JsonResponse({"message": "Este endpoint solo acepta solicitudes POST"}, 
                          status=405)