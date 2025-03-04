from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Credenciais inválidas. Tente novamente.")

    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu do sistema.")
    return redirect('login')