from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction 
from .models import Receita
from .forms import (
    ReceitaForm, 
    IngredienteFormSet,
    EtapaFormSet,
    MidiaFormSet
)

IngredienteFormset = IngredienteFormSet 
EtapaFormset = EtapaFormSet
MidiaFormset = MidiaFormSet

@login_required
def criar_receita(request):
    if request.method == 'POST':
        # Instanciação dos forms e formsets com dados POST
        receita_form = ReceitaForm(request.POST, request.FILES, instance=Receita())
        ingredientes_formset = IngredienteFormset(request.POST, request.FILES, prefix='ingredientes')
        etapas_formset = EtapaFormset(request.POST, request.FILES, prefix='etapas')
        midias_formset = MidiaFormset(request.POST, request.FILES, prefix='midias')
        if (receita_form.is_valid() and 
            ingredientes_formset.is_valid() and 
            etapas_formset.is_valid() and 
            midias_formset.is_valid()):
            with transaction.atomic():
                # 1. Salva a receita principal (sem commit para adicionar o autor)
                receita = receita_form.save(commit=False)
                try:
                    # request.user.perfil é a relação inversa do modelo User para Perfil
                    receita.autor = request.user.perfil 
                except AttributeError:
                    messages.error(request, 'Erro: O perfil do usuário não foi encontrado.')
                    return redirect('home')
                receita.save()
                # 2. Salva os campos ManyToMany (Categorias e Métodos)
                receita_form.save_m2m()
                # 3. Salva os formsets, vinculando-os à receita recém-criada
                ingredientes_formset.instance = receita
                ingredientes_formset.save()
                etapas_formset.instance = receita
                etapas_formset.save()
                midias_formset.instance = receita
                midias_formset.save()
                messages.success(request, 'Receita criada com sucesso!')
                return redirect('home')
        else:
            messages.error(request, 'Houve um erro ao salvar a receita. Verifique os campos.')
    else:
        # Método GET: Instanciação vazia dos forms e formsets
        receita_form = ReceitaForm()
        ingredientes_formset = IngredienteFormset(prefix='ingredientes')
        etapas_formset = EtapaFormset(prefix='etapas')
        midias_formset = MidiaFormset(prefix='midias')
    context = {
        'titulo_pagina': 'Criar Nova Receita',
        'receita_form': receita_form,
        'ingredientes_formset': ingredientes_formset,
        'etapas_formset': etapas_formset,
        'midias_formset': midias_formset,
    }
    return render(request, 'receitas/criar.html', context)

@login_required
def editar_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    if receita.autor.user != request.user:
        messages.error(request, "Você não tem permissão para editar esta receita.")
        return redirect('receitas:detalhe_receita', receita_id=pk)
    if request.method == 'POST':
        receita_form = ReceitaForm(request.POST, request.FILES, instance=receita)
        ingredientes_formset = IngredienteFormset(request.POST, request.FILES, instance=receita, prefix='ingredientes')
        etapas_formset = EtapaFormset(request.POST, request.FILES, instance=receita, prefix='etapas')
        midias_formset = MidiaFormset(request.POST, request.FILES, instance=receita, prefix='midias')
        if (receita_form.is_valid() and ingredientes_formset.is_valid() and 
            etapas_formset.is_valid() and midias_formset.is_valid()):
            with transaction.atomic():
                receita_form.save() # Salva as alterações básicas e ManyToMany
                ingredientes_formset.save() # Atualiza, cria ou deleta ingredientes
                etapas_formset.save()
                midias_formset.save()
                messages.success(request, 'Receita atualizada com sucesso!')
                return redirect('receitas:detalhe_receita', receita_id=receita.pk)
    else:
        receita_form = ReceitaForm(instance=receita)
        ingredientes_formset = IngredienteFormset(instance=receita, prefix='ingredientes')
        etapas_formset = EtapaFormset(instance=receita, prefix='etapas')
        midias_formset = MidiaFormset(instance=receita, prefix='midias')
    context = {
        'titulo_pagina': f'Editar: {receita.nome}',
        'receita_form': receita_form,
        'ingredientes_formset': ingredientes_formset,
        'etapas_formset': etapas_formset,
        'midias_formset': midias_formset,
        'is_edit': True
    }
    return render(request, 'receitas/criar.html', context)

@login_required
def excluir_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    if receita.autor.user != request.user:
        messages.error(request, "Você não tem permissão para excluir esta receita.")
        return redirect('receitas:detalhe_receita', receita_id=pk)
    if request.method == 'POST':
        receita.delete()
        messages.success(request, 'Receita excluída com sucesso.')
        return redirect('usuarios:perfil', username=request.user.username)
    return redirect('receitas:detalhe_receita', receita_id=pk)

def home(request):
    novas_receitas = Receita.objects.filter(estado="PUBLICO").prefetch_related('midias', 'categorias', 'metodos').order_by('-criado_em')[:5]
    return render(request, 'home.html', {'novas_receitas': novas_receitas})

def lista_receitas(request):
    receitas = Receita.objects.filter(estado="PUBLICO").prefetch_related('midias', 'categorias', 'metodos').order_by('-criado_em')
    return render(request, 'receitas/lista.html', {'receitas': receitas})

def detalhe_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    dono = request.user.is_authenticated and request.user == receita.autor.user
    context = {
        'dono': dono,
        'receita': receita,
    }
    return render(request, 'receitas/detalhe.html', context)