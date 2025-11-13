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
            Perfil.objects.create(usuario=user, tipo='USUARIO')
            login(request, user)
            messages.success(request, "Conta criada com sucesso!")
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

def perfil(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    receitas = Receita.objects.filter(autor=perfil)

    context = {
        'perfil': perfil,
        'receitas': receitas,
    }
    return render(request, 'usuarios/perfil.html', context)