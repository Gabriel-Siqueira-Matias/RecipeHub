from django.contrib import admin
from .models import Categoria, Metodo, Receita, Ingrediente, Midia
from django.utils.html import mark_safe
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)

class MetodoAdmin(admin.ModelAdmin):
    list_display = ("nome",)

class IngredienteInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        valid_forms = [
            form for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        ]
        if len(valid_forms) == 0:
            raise ValidationError("Pelo menos um ingrediente é obrigatório.")


class MidiaInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        valid_forms = [
            form for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        ]
        if len(valid_forms) == 0:
            raise ValidationError("Pelo menos uma mídia é obrigatória.")

class IngredienteInline(admin.TabularInline):
    model = Ingrediente
    formset = IngredienteInlineFormSet
    extra = 1

class MidiaInline(admin.TabularInline):
    model = Midia
    formset = MidiaInlineFormSet
    extra = 1
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.tipo == "IMAGEM":
            return mark_safe(f'<img src="{obj.arquivo.url}" style="max-height: 120px; border-radius: 8px;">')
        elif obj.tipo == "VIDEO":
            return mark_safe(f'''
                <video width="220" height="140" controls style="border-radius: 8px;">
                    <source src="{obj.arquivo.url}" type="video/mp4">
                    Seu navegador não suporta a visualização de vídeo.
                </video>
            ''')
        return "—"
    preview.short_description = "Pré-visualização"

class ReceitaAdmin(admin.ModelAdmin):
    list_display = ("nome","autor", "mostrar_categorias", "mostrar_metodos", "tipo", "porcoes", "tempo_preparo", "criado_em")
    search_fields = ("nome",)
    list_filter = ("tipo", "categorias", "metodos", "estado")
    filter_horizontal = ("categorias", "metodos")
    date_hierarchy = "criado_em"
    inlines = [IngredienteInline, MidiaInline]

    def mostrar_categorias(self, obj):
        return ", ".join([c.nome for c in obj.categorias.all()])
    mostrar_categorias.short_description = "Categorias"

    def mostrar_metodos(self, obj):
        return ", ".join([m.nome for m in obj.metodos.all()])
    mostrar_metodos.short_description = "Métodos"

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Metodo, MetodoAdmin)
admin.site.register(Receita, ReceitaAdmin)