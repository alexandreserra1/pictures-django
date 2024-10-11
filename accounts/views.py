# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('login')  # Redirecione para a página de login ou outra página apropriada
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'user_form': form})


# login_view.py
def login_view(request):
    if request.method == 'POST':
        username =  request.POST['username']
        password =  request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pictures_list')  # Redirecione para a página de home ou outra página
        else:
            messages.error(request, 'Credenciais inválidas')
    login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form':login_form})

def logout_view(request):
    logout(request)
    return redirect('pictures_list')  # Redirecione para a página de home ou outra página