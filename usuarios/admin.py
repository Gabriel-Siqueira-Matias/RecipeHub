from django.contrib import admin
from .models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    {}

admin.site.register(Perfil, PerfilAdmin)