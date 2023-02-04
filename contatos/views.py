from django.shortcuts import render

from .models import Contato


# Create your views here.
def index(request):
    contato=Contato.objects.all()
    return render(request,'contatos/index.html',{
        'contatos': contato
    })