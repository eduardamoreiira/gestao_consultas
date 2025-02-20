from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm

# Função para fazer login
def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)  # Verifica se o usuário possui cadastro
        if user is not None:
            login(request, user)
            request.session['username'] = username
            request.session.save()
            return redirect('account:home')
        else:
            # mmensagem de erro
            messages.error(request, 'Usuário não encontrado ou senha incorreta.')
            return redirect('account:login')  # Redireciona de volta para a tela de login
    
    # Se recebermos uma requisição do tipo GET
    return render(request, 'account/login.html', context={})
    

# Função da home
@login_required
def home(request):
    return render(request, 'account/home.html')

# Função para fazer sair do sistema
def signOut(request):
    logout(request)
    return render(request=request, template_name='account/login.html', context={}) 

# Função de registro
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso. Faça login.')
            return redirect('account:signIn')
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})
