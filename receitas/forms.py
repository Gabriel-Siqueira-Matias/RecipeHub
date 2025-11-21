from django import forms
from django.forms.models import inlineformset_factory
from .models import Receita, Ingrediente, Etapa, Midia, Categoria, Metodo

class ReceitaForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Categorias"
    )
    metodos = forms.ModelMultipleChoiceField(
        queryset=Metodo.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Métodos"
    )
    tipo = forms.ChoiceField(
        choices=Receita.TIPOS,
        widget=forms.RadioSelect,
        label="Tipo"
    )
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
        }
IngredienteFormSet = inlineformset_factory(
    Receita, 
    Ingrediente, 
    fields=['nome', 'quantidade', 'unidade', 'opcional'],
    can_delete=True,
    widgets={
        'nome': forms.TextInput(attrs={'placeholder': 'Ex: Açúcar'}),
        'quantidade': forms.NumberInput(attrs={'placeholder': 'Ex: 1'}),
        'unidade': forms.Select(attrs={'class': 'select-unidade'}),
    }
)
EtapaFormSet = inlineformset_factory(
    Receita, 
    Etapa, 
    fields=['conteudo'],
    extra=1,
    can_delete=True,
    widgets={
        'conteudo': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descreva o passo de preparo.'}),
    }
)
MidiaFormSet = inlineformset_factory(
    Receita, 
    Midia, 
    fields=['tipo', 'arquivo'],
    extra=1,
    can_delete=True,
    widgets={
        'tipo': forms.Select(attrs={'class': 'select-tipo-midia'}),
    }
)