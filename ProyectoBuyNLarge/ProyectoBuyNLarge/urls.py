from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from chatbot.views import ChatBotView

urlpatterns = [
    # Rutas de API
    path('admin/', admin.site.urls),
    path('chatbot/', include('chatbot.urls')),
    path('api/users/', include('users.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/chatbot/', ChatBotView.as_view(), name='chatbot'),

    # Ruta para React
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),

]
