from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Categoria, Metodo

@receiver(post_migrate)
def criar_categorias_metodos_padrao(sender, **kwargs):
    if sender.name == "receitas":

        categorias = ["Prato Principal", "Sobremesa", "Lanche", "Aperitivo", "Bebida", "Acompanhemento", "Outro", "Quente", "Frio"]
        for nome in categorias:
            Categoria.objects.get_or_create(nome=nome)

        metodos = ["Assado", "Frito", "Cozido", "Grelhado", "Cru", "Fogo Lento", "Rápido", "Batido"]
        for nome in metodos:
            Metodo.objects.get_or_create(nome=nome)
