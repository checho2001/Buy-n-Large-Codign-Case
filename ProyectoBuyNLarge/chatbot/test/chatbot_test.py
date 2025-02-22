import requests
import json

def test_chatbot_endpoint():
    # URL del endpoint (ajusta según tu configuración)
    url = "http://localhost:8000/chatbot/v1/make_question/"
    
    # Datos de la solicitud
    payload = {
        "message": "¿Cuáles Smartphone Apple tienes en inventario?"
    }
    
    # Cabeceras
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Realizar la solicitud POST
        response = requests.post(url, json=payload, headers=headers)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()
            print("\nRespuesta del chatbot:")
            print("-" * 50)
            print(f"Respuesta: {data['response']}")
            print(f"Cantidad de resultados: {data['results_count']}")
        else:
            print(f"\nError: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"\nError de conexión: {e}")

if __name__ == "__main__":
    print("Enviando solicitud al chatbot...")
    test_chatbot_endpoint()