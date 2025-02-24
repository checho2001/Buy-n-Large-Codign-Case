# Proyecto BuyNLarge

Este proyecto es una aplicación de comercio electrónico que permite a los usuarios interactuar con un chatbot para obtener recomendaciones de productos y realizar compras. El backend está construido con Django y Django REST Framework.

## Tabla de Contenidos

- [Características](#características)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
- [Modelos](#modelos)
- [Pruebas](#pruebas)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Características

- Interacción con un chatbot para obtener recomendaciones de productos.
- Gestión de productos y órdenes de compra.
- API RESTful para la comunicación entre el frontend y el backend.

## Tecnologías Utilizadas

- Django 5.x
- Django REST Framework
- PostgreSQL (o SQLite para desarrollo)
- Python 3.x
- Otras dependencias especificadas en `requirements.txt`

## Estructura del Proyecto

El proyecto está organizado en varias aplicaciones:

- **chatbot**: Maneja la lógica del chatbot, incluyendo sesiones de chat y mensajes.
- **inventory**: Gestiona los productos y órdenes de compra.

### Estructura de Carpetas

```
ProyectoBuyNLarge/
│
├── chatbot/                # Aplicación del chatbot
│   ├── admin.py
│   ├── apps.py
│   ├── models/
│   ├── serializers.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/         # Migraciones de la base de datos
│
├── inventory/              # Aplicación de inventario
│   ├── admin.py
│   ├── apps.py
│   ├── models/
│   ├── serializers.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/         # Migraciones de la base de datos
│
├── fixtures/               # Datos de prueba
│   └── precharge-products.json
│
├── .gitignore              # Archivos y carpetas a ignorar por Git
├── manage.py               # Script de gestión de Django
└── requirements.txt        # Dependencias del proyecto
```

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/ProyectoBuyNLarge.git
   cd ProyectoBuyNLarge
   ```

2. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno en un archivo `.env`.

5. Realiza las migraciones:
   ```bash
   python manage.py migrate
   ```

6. Carga los datos iniciales (opcional):
   ```bash
   python manage.py loaddata fixtures/precharge-products.json
   ```

7. Inicia el servidor:
   ```bash
   python manage.py runserver
   ```

## Uso

- Accede a la API del chatbot en `http://localhost:8000/chatbot/v1/make_question/`.
- Utiliza herramientas como Postman o cURL para interactuar con los endpoints de la API.

## Modelos

### ChatMessage

- `message_text`: Texto del mensaje.
- `is_bot`: Indica si el mensaje es del bot.
- `created_at`: Fecha y hora de creación.

### ChatSession

- `user`: Usuario asociado a la sesión.
- `created_at`: Fecha y hora de creación.
- `ended_at`: Fecha y hora de finalización.

### Product

- `name`: Nombre del producto.
- `brand`: Marca del producto.
- `category`: Categoría del producto.
- `price`: Precio del producto.
- `stock`: Cantidad disponible.

### Order

- `user`: Usuario que realiza la orden.
- `product`: Producto asociado a la orden.
- `quantity`: Cantidad del producto.
- `total_price`: Precio total de la orden.
- `status`: Estado de la orden.

##Cargue de Productos
python manage.py loaddata fixtures/precharge-products.json

## Contribuciones

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu característica o corrección de errores.
3. Realiza tus cambios y asegúrate de que las pruebas pasen.
4. Envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

