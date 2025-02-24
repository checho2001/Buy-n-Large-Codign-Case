# Proyecto BuyNLarge

Este proyecto es una aplicación de comercio electrónico que permite a los usuarios interactuar con un chatbot para obtener recomendaciones de productos y realizar compras. El proyecto está dividido en dos partes: el frontend, construido con React, y el backend, construido con Django.

## Tabla de Contenidos

- [Frontend](#frontend)
  - [Características](#características-frontend)
  - [Instalación](#instalación-frontend)
  - [Uso](#uso-frontend)
  - [Estructura del Proyecto](#estructura-del-proyecto-frontend)
- [Backend](#backend)
  - [Características](#características-backend)
  - [Instalación](#instalación-backend)
  - [Estructura del Proyecto](#estructura-del-proyecto-backend)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Frontend

### Características

- Interfaz de usuario interactiva para la compra de productos.
- Integración con el chatbot para obtener recomendaciones.
- Uso de React y Tailwind CSS para un diseño moderno y responsivo.

### Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/ProyectoBuyNLarge.git
   cd ProyectoBuyNLarge/frontend
   ```

2. Instala las dependencias:
   ```bash
   npm install
   ```

### Uso

Para iniciar la aplicación en modo de desarrollo, ejecuta:
```bash
npm start
```
Abre [http://localhost:3000](http://localhost:3000) en tu navegador para ver la aplicación.

### Estructura del Proyecto

```
frontend/
│
├── public/                # Archivos públicos
│   ├── index.html
│   ├── manifest.json
│   └── robots.txt
│
├── src/                   # Código fuente de la aplicación
│   ├── components/        # Componentes de React
│   ├── App.js             # Componente principal
│   └── App.css            # Estilos globales
│
├── package.json           # Dependencias y scripts
└── .gitignore             # Archivos a ignorar por Git
```

## Backend

### Características

- API RESTful para la gestión de productos y órdenes.
- Integración con un chatbot para la interacción del usuario.
- Uso de Django y Django REST Framework.

### Instalación

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

### Estructura del Proyecto

```
ProyectoBuyNLarge/
│
├── chatbot/               # Aplicación del chatbot
│   ├── models/            # Modelos de datos
│   ├── views.py           # Vistas de la API
│   └── serializers.py     # Serializadores de datos
│
├── inventory/             # Aplicación de inventario
│   ├── models/            # Modelos de productos y órdenes
│   ├── views.py           # Vistas de la API
│   └── serializers.py     # Serializadores de datos
│
├── fixtures/              # Datos de prueba
│   └── precharge-products.json
│
├── manage.py              # Script de gestión de Django
└── requirements.txt       # Dependencias del proyecto
```

## Contribuciones

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu característica o corrección de errores.
3. Realiza tus cambios y asegúrate de que las pruebas pasen.
4. Envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

