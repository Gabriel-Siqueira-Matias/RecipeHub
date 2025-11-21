from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import Formulario_Cadastro
from django.contrib.auth.views import LoginView
from .models import Perfil
from receitas.models import Receita
from django.shortcuts import render, get_object_or_404

def cadastro(request):
    if request.method == 'POST':
        form = Formulario_Cadastro(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = Formulario_Cadastro()
    return render(request, 'usuarios/cadastro.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('home')
    
def logout_view(request):
    logout(request)
    return redirect('home')

def perfil(request, username):
    dono_perfil = get_object_or_404(Perfil, user__username=username)
    dono = request.user.is_authenticated and request.user == dono_perfil.user
    receitas = Receita.objects.prefetch_related('midias', 'categorias', 'metodos').filter(autor=dono_perfil)
    receitas_publicas = receitas.prefetch_related('midias', 'categorias', 'metodos').filter(estado="PUBLICO")
    if dono:
        novas_receitas = receitas.prefetch_related('midias', 'categorias', 'metodos').order_by('-criado_em')[:5]
    else:
        novas_receitas = receitas_publicas.prefetch_related('midias', 'categorias', 'metodos').order_by('-criado_em')[:5]
    context = {
        'dono_perfil': dono_perfil,
        'dono': dono,
        'receitas': receitas,
        'receitas_publicas': receitas_publicas,
        'novas_receitas': novas_receitas,
    }
    return render(request, 'usuarios/perfil.html', context)

def lista_receitas_perfil(request, username):
    dono_perfil = get_object_or_404(Perfil, user__username=username)
    dono = request.user.is_authenticated and request.user == dono_perfil.user
    if dono:
        receitas = Receita.objects.prefetch_related('midias', 'categorias', 'metodos').filter(autor=dono_perfil)
    else:
        receitas = Receita.objects.prefetch_related('midias', 'categorias', 'metodos').filter(autor=dono_perfil, estado="PUBLICO")
    context = {
        'receitas': receitas,
        'dono_perfil': dono_perfil,
        'dono': dono,
    }
    return render(request, 'usuarios/lista_perfil.html', context)