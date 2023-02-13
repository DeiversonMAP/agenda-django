from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import \
    validate_email  # validador de emails do django
from django.shortcuts import redirect, render


# Create your views here.
def login(request):
    return render(request,'accounts/login.html')

def logout(request):
    return render(request,'accounts/logout.html')

def register(request):
    if request.method != 'POST':
        return render(request,'accounts/register.html')
    
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    
    if not nome or not sobrenome or not email or not usuario or not senha or not senha2 :
        messages.error(request,'Nenhum campo pode estar vazio.')
        return render(request,'accounts/register.html')
    
    #validação do email
    try:
        validate_email(email)
    except:
        messages.error(request,'Email invalido.')
        return render(request,'accounts/register.html')

    if len(usuario) < 6:
        messages.error(request,'Usuário precisa ter 6 caracteres ou mais.')
        return render(request,'accounts/register.html')
    if len(senha) < 6:
        messages.error(request,'Senha precisa ter 6 caracteres ou mais.')
        return render(request,'accounts/register.html')
    if senha != senha2:
        messages.error(request,'Senhas diferentes.')
        return render(request,'accounts/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request,'Usuário já existe.')
        return render(request,'accounts/register.html')
    
    if User.objects.filter(email=email).exists():
        messages.error(request,'E-mail já existe.')
        return render(request,'accounts/register.html')

    messages.success(request,'Registrado com sucesso! Agora faça login com as informações usados no cadastro')
    user = User.objects.create_user(username=usuario,email=email,
                                    password=senha,first_name=nome,last_name=sobrenome)
    user.save()
    return redirect('login')

def dashboard(request):
    return render(request,'accounts/dashboard.html')
