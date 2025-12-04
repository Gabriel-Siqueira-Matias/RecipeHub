from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView

app_name = "usuarios"

urlpatterns = [
    path("cadastro/", views.cadastro, name="cadastro"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/<str:username>/', views.perfil, name='perfil'),
    path('perfil/<str:username>/lista/', views.lista_receitas_perfil, name='lista_perfil'),
    path('perfil/<str:username>/favoritos/', views.lista_favoritos_perfil, name='lista_favoritos_perfil'),
]