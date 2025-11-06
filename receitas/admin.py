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
    list_display = ("nome", "mostrar_categorias", "mostrar_metodos", "tipo", "porcoes", "tempo_preparo", "criado_em")
    list_filter = ("tipo", "categorias", "metodos")
    search_fields = ("nome",)
    filter_horizontal = ("categorias", "metodos")
    data_hierarchy = 'criado_em'
    inlines = [IngredienteInline]

    def mostrar_categorias(self, obj):
        return ", ".join([c.nome for c in obj.categorias.all()])
    mostrar_categorias.short_description = "Categorias"

    def mostrar_metodos(self, obj):
        return ", ".join([m.nome for m in obj.metodos.all()])
    mostrar_metodos.short_description = "Métodos"

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Metodo, MetodoAdmin)
admin.site.register(Receita, ReceitaAdmin)