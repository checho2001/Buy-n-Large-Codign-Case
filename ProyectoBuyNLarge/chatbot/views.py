from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer

class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        session = self.get_object()
        message_text = request.data.get('message_text', '')
        is_bot = request.data.get('is_bot', False)
        product_id = request.data.get('product', None)

        message = ChatMessage.objects.create(
            session=session,
            message_text=message_text,
            is_bot=is_bot,
            product_id=product_id,
        )
        serializer = ChatMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def get_messages(self, request, pk=None):
        session = self.get_object()
        messages = ChatMessage.objects.filter(session=session)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def end_session(self, request, pk=None):
        session = self.get_object()
        session.ended_at = timezone.now()
        session.save()
        return Response({'message': 'Sesión finalizada'}, status=status.HTTP_200_OK)

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

