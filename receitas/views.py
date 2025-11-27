from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction 
from .models import Receita
from .forms import (
    Receita_Formulario, 
    Ingrediente_FormSet,
    Etapa_FormSet,
    Midia_FormSet,
)

@login_required(redirect_field_name='next', login_url='usuarios:login')
def criar_receita(request):
    if request.method == 'POST':
        receita_formulario = Receita_Formulario(request.POST)
        ingredientes_formset = Ingrediente_FormSet(request.POST)
        midias_formset = Midia_FormSet(request.POST, request.FILES)
        etapas_formset = Etapa_FormSet(request.POST)
        if (receita_formulario.is_valid() and ingredientes_formset.is_valid() and etapas_formset.is_valid() and midias_formset.is_valid()):
            try:
                with transaction.atomic():
                    nova_receita = receita_formulario.save(commit=False)
                    nova_receita.autor = request.user.perfil
                    nova_receita.save()
                    receita_formulario.save_m2m()
                    ingredientes_formset.instance = nova_receita
                    ingredientes_formset.save()
                    midias_formset.instance = nova_receita
                    midias_formset.save()
                    etapas_formset.instance = nova_receita
                    etapas_formset.save()
                messages.success(request, 'Receita criada com sucesso!')
                return redirect('usuarios:perfil', username=request.user.username)
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao salvar a receita. Tente novamente. Detalhe: {e}')
        else:
            messages.error(request, 'Houve um erro no preenchimento do formulário.')
            context = {
                'titulo_pagina': 'Criar Nova Receita',
                'receita_formulario': receita_formulario,
                'ingredientes_formset': ingredientes_formset,
                'etapas_formset': etapas_formset,
                'midias_formset': midias_formset,
            }
            return render(request, 'receitas/criar.html', context)
    else:
        context = {
            'titulo_pagina': 'Criar Nova Receita',
            'receita_formulario': Receita_Formulario(),
            'ingredientes_formset': Ingrediente_FormSet(),
            'etapas_formset': Etapa_FormSet(),
            'midias_formset': Midia_FormSet(),
        }
        return render(request, 'receitas/criar.html', context)
    
@login_required(redirect_field_name='next', login_url='usuarios:login')
def editar_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    if receita.autor != request.user.perfil:
        messages.error(request, "Você não possui permissão para editar essa receita")
        return redirect('receitas:detalhe_receita', receita_id=receita_id)
    if request.method == 'POST':
        receita_formulario = Receita_Formulario(request.POST, instance=receita)
        ingredientes_formset = Ingrediente_FormSet(request.POST, instance=receita)
        midias_formset = Midia_FormSet(request.POST, request.FILES, instance=receita)
        etapas_formset = Etapa_FormSet(request.POST, instance=receita)
        if (receita_formulario.is_valid() and ingredientes_formset.is_valid() and etapas_formset.is_valid() and midias_formset.is_valid()):
            try:
                with transaction.atomic():
                    receita_formulario.save()
                    ingredientes_formset.save()
                    midias_formset.save()
                    etapas_formset.save()
                messages.success(request, f'Receita "{receita.nome}" atualizada com sucesso!')
                return redirect('usuarios:perfil', username=request.user.username)
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao salvar as alterações da receita. Tente novamente. Detalhe: {e}')
        else:
            messages.error(request, 'Houve um erro no preenchimento do formulário.')
    context = {
        'titulo_pagina': f'Editar Receita: {receita.nome}',
        'receita_formulario': Receita_Formulario(instance=receita),
        'ingredientes_formset': Ingrediente_FormSet(instance=receita),
        'etapas_formset': Etapa_FormSet(instance=receita),
        'midias_formset': Midia_FormSet(instance=receita),
        'modo_edicao': True,
    }
    return render(request, 'receitas/criar.html', context)

@login_required
def excluir_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    if receita.autor != request.user.perfil:
        messages.error(request, "Você não tem permissão para excluir esta receita.")
        return redirect('receitas:detalhe_receita', receita_id=receita_id)
    if request.method == 'POST':
        receita.delete()
        messages.success(request, 'Receita excluída com sucesso.')
        return redirect('usuarios:perfil', username=request.user.username)
    return redirect('receitas:detalhe_receita', receita_id=receita_id)

@login_required
def favoritar_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    perfil = request.user.perfil
    if receita.autor == perfil:
        messages.error(request, "Você não pode favoritar sua propria receita.")
        return redirect('receitas:detalhe_receita', receita_id=receita_id)
    if perfil.favoritos.filter(id=receita_id).exists():
        perfil.favoritos.remove(receita)
        messages.info(request, f'"{receita.nome}" removida dos seus favoritos.')
    else:
        perfil.favoritos.add(receita)
        messages.success(request, f'"{receita.nome}" adicionada aos seus favoritos!')
    return redirect('receitas:detalhe_receita', receita_id=receita_id)

def home(request):
    novas_receitas = Receita.objects.filter(estado="PUBLICO").prefetch_related('midias', 'categorias', 'metodos').order_by('-criado_em')[:5]
    return render(request, 'home.html', {'novas_receitas': novas_receitas})

def lista_receitas(request):
    receitas = Receita.objects.filter(estado="PUBLICO").prefetch_related('midias', 'categorias', 'metodos').order_by('-criado_em')
    return render(request, 'receitas/lista.html', {'receitas': receitas})

def detalhe_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    dono = request.user.is_authenticated and request.user == receita.autor.user
    favoritado = False
    if request.user.is_authenticated and hasattr(request.user, 'perfil'):
        favoritado = request.user.perfil.favoritos.filter(id=receita.pk).exists()
    context = {
        'dono': dono,
        'receita': receita,
    }
    return render(request, 'receitas/detalhe.html', context)