import requests
import json
import uuid

def test_chatbot_endpoint(session_id=None):
    # URL del endpoint (verificar que coincida con tus rutas)
    url = "http://localhost:8000/chatbot/v1/make_question/"  # Ajustar según tu urls.py
    
    # Payload dinámico para manejar sesiones existentes o nuevas
    payload = {
        "message": "¿Tienes computadoras de otra marca?",
    }
    
    # Si se provee session_id, lo agregamos al payload
    if session_id:
        payload["session_id"] = str(session_id)
        print(f"\nUsando sesión existente: {session_id}")
    else:
        print("\nIniciando nueva sesión...")
    
    headers = {
        "Content-Type": "application/json",
        # Si tienes autenticación, agregar aquí el token:
        # "Authorization": f"Bearer {YOUR_TOKEN}"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            _print_response(data, session_id is None)
            
            # Retornar session_id para usar en pruebas consecutivas
            return data.get('session_id')
            
        else:
            print(f"\nError: {response.status_code}")
            print(response.text)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\nError de conexión: {e}")
        return None

def _print_response(data, is_new_session):
    """Helper para formatear la salida"""
    print("\nRespuesta del chatbot:")
    print("-" * 50)
    if is_new_session:
        print(f"[Nueva sesión creada: {data['session_id']}]")
    print(f"Respuesta: {data['response']}")
    print(f"Resultados encontrados: {data['results_count']}")
    print("-" * 50)

def test_multiple_messages():
    """Prueba de conversación completa"""
    print("\n=== Test de conversación completa ===")
    
    # Primer mensaje
    session_id = test_chatbot_endpoint()
    
    if session_id:
        # Segundo mensaje usando misma sesión
        print("\nSegundo mensaje (misma sesión)")
        test_chatbot_endpoint(session_id)
        
        # Tercer mensaje con contexto
        print("\nTercer mensaje con contexto)")
        test_chatbot_endpoint(session_id)

def test_edge_cases():
    """Prueba casos límite"""
    print("\n=== Test de casos límite ===")
    
    # Mensaje vacío
    print("\nTest mensaje vacío:")
    test_chatbot_endpoint_with_custom_payload({"message": ""})
    
    # Session ID inválido
    print("\nTest session_id inválido:")
    test_chatbot_endpoint(session_id=uuid.uuid4())

def test_chatbot_endpoint_with_custom_payload(custom_payload):
    """Versión para pruebas personalizadas"""
    url = "http://localhost:8000/chatbot/v1/make_question/"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=custom_payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("=== Test Básico ===")
    basic_test_id = test_chatbot_endpoint(session_id='1aa3283f-ec81-498d-b7d2-311c47f30fcb')
    
    # Descomentar para pruebas avanzadas
    # test_multiple_messages()
    # test_edge_cases()