from django.urls import path
from . import views

app_name = 'receitas'

urlpatterns = [
    path('lista/', views.lista_receitas, name='lista_receitas'),
    path('favoritos/', views.lista_favoritos, name='lista_favoritos'),
    path('<int:receita_id>/', views.detalhe_receita, name='detalhe_receita'),
    path("criar/", views.criar_receita, name="criar_receita"),
    path('editar/<int:receita_id>/', views.editar_receita, name='editar_receita'),
    path('excluir/<int:receita_id>/', views.excluir_receita, name='excluir_receita'),
    path('favoritar/<int:receita_id>/', views.favoritar_receita, name='favoritar_receita'),
    path('pesquisar/', views.pesquisar_receita, name='pesquisar_receita'),
]