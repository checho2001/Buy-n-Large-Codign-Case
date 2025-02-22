from django.urls import path

from .views import ChatBotView

urlpatterns = [
    path('v1/make_question/', ChatBotView.as_view(), name='chatbot'),
]