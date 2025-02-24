from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'users/login.html')

class RoleView(APIView):
    def get(self, request):
        # Obtener el username del query param si existe, sino usar el usuario autenticado
        username = request.GET.get('user', request.user.username)
        
        try:
            # Usar get() en lugar de filter() para obtener un único objeto
            user = CustomUser.objects.get(username=username)
            return Response({'role': user.role})
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'}, 
                status=404
            )
