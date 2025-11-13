from django.shortcuts import render, get_object_or_404
from .models import Receita

def home(request):
    novas_receitas = Receita.objects.filter(estado="PUBLICO").prefetch_related().order_by('-criado_em')[:5]
    return render(request, 'home.html', {'novas_receitas': novas_receitas})

def lista_receitas(request):
    receitas = Receita.objects.filter(estado="PUBLICO").prefetch_related().order_by('-criado_em')
    return render(request, 'receitas/lista.html', {'receitas': receitas})

def detalhe_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    return render(request, 'receitas/detalhe.html', {'receita': receita})