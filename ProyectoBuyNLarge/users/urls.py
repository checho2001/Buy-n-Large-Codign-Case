from django.urls import path
from . import views
from .views import RoleView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('role/', RoleView.as_view(), name='role'),
]