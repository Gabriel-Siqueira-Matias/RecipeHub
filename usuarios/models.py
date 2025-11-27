from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    TIPOS = [
        ('ADMIN', 'Administrador'),
        ('USUARIO', 'Usuário'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='USUARIO')
    favoritos = models.ManyToManyField('receitas.Receita', related_name="usuarios_favorito", verbose_name="Favoritos", blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_tipo_display()})"