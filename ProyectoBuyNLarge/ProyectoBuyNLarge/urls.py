from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from chatbot.views import ChatBotView

urlpatterns = [
    # Rutas de API
    path('admin/', admin.site.urls),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/metrics/', include('metrics.urls')),
    path('api/users/', include('users.urls')),
    # Ruta para React
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),

]
