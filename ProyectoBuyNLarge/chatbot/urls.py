from django.urls import path
from .views import ChatBotView, ChatBotViewSet

urlpatterns = [
    path('v1/make_question/', ChatBotView.as_view(), name='chatbot'),
    path('api/chatbot/', ChatBotView.as_view(), name='chatbot'),
    path('api/chatbot/conversations/', ChatBotViewSet.as_view({'get': 'get_conversations'}), name='conversations'),
    path('api/chatbot/messages/<uuid:conversation_id>/', ChatBotViewSet.as_view({'get': 'get_messages'}), name='messages'),
    #path('chat/history/<uuid:session_id>/', get_chat_history, name='get_chat_history'),
]