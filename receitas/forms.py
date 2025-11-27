from django import forms
from django.forms.models import inlineformset_factory
from .models import Receita, Ingrediente, Etapa, Midia, Categoria, Metodo

class Receita_Formulario(forms.ModelForm):
    class Meta:
        model = Receita
        fields = [
            'nome', 
            'categorias', 
            'metodos', 
            'tipo', 
            'porcoes', 
            'tempo_preparo', 
            'estado'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Bolo de Chocolate Clássico'}),
            'porcoes': forms.NumberInput(attrs={'placeholder': 'Ex: 8'}),
            'tempo_preparo': forms.NumberInput(attrs={'placeholder': 'Ex: 45'}),
            'categorias': forms.CheckboxSelectMultiple(),
            'metodos': forms.CheckboxSelectMultiple(),
            'tipo': forms.RadioSelect(),
        }

class Ingrediente_Formulario(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = [
            'nome',
            'quantidade',
            'unidade',
            'opcional',
        ]
        widgets={
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Açúcar'}),
            'quantidade': forms.NumberInput(attrs={'placeholder': 'Ex: 5 ou 0.5', 'step': '0.01'}),
            'unidade': forms.Select(),
        }

Ingrediente_FormSet = inlineformset_factory(
    Receita, Ingrediente, form=Ingrediente_Formulario, extra=1, can_delete=True
)

class Etapa_Formulario(forms.ModelForm):
    class Meta:
        model = Etapa
        fields = [
            'conteudo'
        ]
        widgets={
            'conteudo': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Descreva a etapa de preparo.'}),
        }

Etapa_FormSet = inlineformset_factory(
    Receita, Etapa, form=Etapa_Formulario, extra=1, can_delete=True
)

class Midia_Formulario(forms.ModelForm):
    class Meta:
        model = Midia
        fields = [
            'tipo',
            'arquivo',
        ]

Midia_FormSet = inlineformset_factory(
    Receita, Midia, form=Midia_Formulario, extra=1, can_delete=True
)