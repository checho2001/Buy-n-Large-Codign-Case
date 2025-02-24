from rest_framework import serializers
from .models import ChatSession, ChatMessage

#chat session serializer
class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'created_at', 'ended_at']

#chat message serializer
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'message_text', 'is_bot', 'product', 'created_at']

