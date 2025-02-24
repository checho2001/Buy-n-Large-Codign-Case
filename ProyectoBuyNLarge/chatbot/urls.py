from django.urls import path
from .views import ChatBotView, ChatBotViewSet

urlpatterns = [
    # Ruta principal para el chatbot
    path('', ChatBotView.as_view(), name='chatbot'),
    
    # Rutas para gestión de conversaciones
    path('api/chatbot/conversations/', 
         ChatBotViewSet.as_view({
             'get': 'list',
             'post': 'create'
         }), 
         name='conversations'),
    
    # Ruta para mensajes de una conversación específica
    path('api/chatbot/conversations/<str:pk>/messages/', 
         ChatBotViewSet.as_view({
             'get': 'messages'
         }), 
         name='conversation-messages'),
    #path('chat/history/<uuid:session_id>/', get_chat_history, name='get_chat_history'),
]