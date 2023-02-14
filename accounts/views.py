from django.contrib import auth, messages
from django.contrib.auth.decorators import \
    login_required  # decorator para dizer que login é necessario para acesso
from django.contrib.auth.models import User
from django.core.validators import \
    validate_email  # validador de emails do django
from django.shortcuts import redirect, render

from .models import FormContato


# Create your views here.
def login(request):
    if request.method != 'POST':
        return render(request,'accounts/login.html')    
    
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user =auth.authenticate(request,username=usuario,password=senha) #retorna None se estiver incorreto
    if not user:
        messages.error(request,'Nome de usuário ou senha inválidos.')
        return render(request,'accounts/login.html')  
    else:
        auth.login(request,user)
        messages.success(request,'Logado com sucesso!')
        return redirect('dashboard')

def logout(request):
    auth.logout(request)
    messages.success(request,'Logout feito com sucesso')
    return redirect('login')

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

@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request,'accounts/dashboard.html',{'form':form})
    
    form = FormContato(request.POST,request.FILES)
    
    # if form.is_valid(): form.save() # validação do próprio django
    
    if not form.is_valid():
        messages.error(request,"Erro ao enviar formulário.")
        form = FormContato(request.POST)
        return render(request,'accounts/dashboard.html',{'form':form})
    
    if len(descricao := request.POST.get('descricao')) <5:
        messages.error(request,"Descrição precisa ter mais que 5 caracteres.")
        form = FormContato(request.POST)
        return render(request,'accounts/dashboard.html',{'form':form})

    form.save() # salvar o formulário
    messages.success(request,f"Contato {request.POST.get('nome')} salvo com sucesso!!")
    return redirect('dashboard')