from django import \
    forms  # biblioteca para o próprio django gerar o form do model
from django.db import models

from contatos.models import Contato


class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        exclude = ("mostrar",) # tupla para retirar os campos que nao devem ir para o form