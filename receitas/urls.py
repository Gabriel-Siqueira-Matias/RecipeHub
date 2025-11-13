from django.urls import path
from . import views

app_name = 'receitas'

urlpatterns = [
    path('lista/', views.lista_receitas, name='lista_receitas'),
    path('<int:receita_id>/', views.detalhe_receita, name='detalhe_receita'),
]