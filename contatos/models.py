from django.db import models
from django.utils import timezone

# Create your models here.

# Os ids das tabelas são gerados automaticamente
class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    
    #metodo criado para alterar a representaçãp do objeto dentro do admin
    def __str__(self) -> str: 
        return self.nome

class Contato(models.Model):
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255, blank=True)
    telefone = models.CharField(max_length=11)
    email = models.CharField(max_length=255,blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    mostrar = models.BooleanField(default=True)

    def __str__(self) -> str: 
        return f'{self.nome.title()} {self.sobrenome.title()} - {self.categoria.nome}'
        # return self.nome + ' ' + self.sobrenome
