from django.core.paginator import Paginator
from django.db.models import (  # importação para poder fazer consultas mais complexas, como utilizar OR nos filtros
    Q, Value)
from django.db.models.functions import Concat  # Biblioteca de funções SQL
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Contato


# Create your views here.
def index(request):
    # contatos = Contato.objects.all()
    # contatos = Contato.objects.order_by('id') #Ordem crescente
    # contatos = Contato.objects.order_by('-id') #Ordem decrescente
    contatos = Contato.objects.order_by('id').filter(mostrar=True) # Filtrando contatos que tenham o campo mostrar igual a True
    
    # https://docs.djangoproject.com/en/2.2/topics/pagination/
    paginator = Paginator(contatos,20)
    page = request.GET.get('p')
    
    contatos = paginator.get_page(page)
    return render(request,'contatos/index.html',{
        'contatos': contatos
    })
    
def ver_contato(request,contato_id):
    # contato=Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato,id=contato_id)
    
    if not contato.mostrar:
        raise Http404()

    return render(request,'contatos/ver_contato.html',{
        'contato': contato
        })

def busca(request):
    termo = request.GET.get('termo')
    
    if termo is None :
        raise Http404()
    # contatos = Contato.objects.filter(mostrar=True,nome=termo) # Filtrando busca pelo valor passado no termo
    # contatos = Contato.objects.order_by('id').filter(
    #     Q(nome__icontains=termo) | Q(sobrenome__icontains=termo), # Filtrando busca em que contenha o valor passado no termo
    #     mostrar=True,                                             # Porém esse filtro não é tão util, pois nao permite 
    #     )                                                         # buscar o nome completo
    concat=Concat('nome',Value(' '),'sobrenome')
    contatos= Contato.objects.order_by('id').annotate(
        nome_completo=concat
    ).filter(
        Q(nome_completo__icontains=termo) |
        Q(telefone__contains=termo)
    )
    
    paginator = Paginator(contatos,20)
    page = request.GET.get('p')
    
    contatos = paginator.get_page(page)
    return render(request,'contatos/busca.html',{
        'contatos': contatos
    })