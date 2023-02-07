from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Contato


# Create your views here.
def index(request):
    # contatos = Contato.objects.all()
    # contatos = Contato.objects.order_by('id') #Ordem crescente
    # contatos = Contato.objects.order_by('-id') #Ordem decrescente
    contatos = Contato.objects.order_by('id').filter(mostrar=True) # Filtranto contatos que tenham o campo mostrar igual a True
    
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
