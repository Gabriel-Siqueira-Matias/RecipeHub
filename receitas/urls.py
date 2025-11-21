from django.urls import path
from . import views

app_name = 'receitas'

urlpatterns = [
    path('lista/', views.lista_receitas, name='lista_receitas'),
    path('<int:receita_id>/', views.detalhe_receita, name='detalhe_receita'),
    path("criar/", views.criar_receita, name="criar_receita"),
    path('editar/<int:pk>/', views.editar_receita, name='editar'),
    path('excluir/<int:pk>/', views.excluir_receita, name='excluir'),
]