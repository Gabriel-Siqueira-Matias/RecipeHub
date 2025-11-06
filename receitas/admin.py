from django.contrib import admin
from .models import Categoria, Metodo, Receita, Ingrediente

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)

class MetodoAdmin(admin.ModelAdmin):
    list_display = ("nome",)

class IngredienteInline(admin.TabularInline):
    model = Ingrediente
    extra = 1

class ReceitaAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "porcoes", "tempo_preparo", "criado_em")
    list_filter = ("tipo", "categorias", "metodos")
    search_fields = ("nome",)
    filter_horizontal = ("categorias", "metodos")
    inlines = [IngredienteInline]

class IngredienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "quantidade", "unidade", "receita")
    list_filter = ("unidade",)

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Metodo, MetodoAdmin)
admin.site.register(Receita, ReceitaAdmin)
admin.site.register(Ingrediente, IngredienteAdmin)