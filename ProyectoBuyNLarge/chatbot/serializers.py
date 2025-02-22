from rest_framework import serializers
from .models import ChatSession, ChatMessage

class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'created_at', 'ended_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'message_text', 'is_bot', 'product', 'created_at']


