from django.contrib import admin

# Register your models here.
from .models import Categoria, Contato


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id','nome', 'sobrenome','telefone','email','categoria', 'data_criacao','mostrar')
    list_display_links = ('nome', 'sobrenome')
    # list_filter = ('categoria',)
    list_per_page = 10
    search_fields = ('nome', 'sobrenome', 'categoria')
    list_editable = ('telefone','mostrar')
    
    
admin.site.register(Categoria) 
admin.site.register(Contato, ContatoAdmin)
