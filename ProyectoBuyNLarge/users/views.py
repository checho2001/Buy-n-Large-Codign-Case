from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from chatbot.models import ChatSession  # Asegúrate de importar el modelo ChatSession

#login view
def login_view(request):
    #login view
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Crear una nueva sesión de chat
            chat_session = ChatSession.objects.create(user=user)
            # Guardar el session_id en la sesión del usuario
            request.session['session_id'] = str(chat_session.id)
            messages.success(request, 'Has iniciado sesión correctamente.')
            return redirect('home')  # Redirige a la página de inicio
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'users/login.html')