from django.db import models
from usuarios.models import Perfil

class Categoria(models.Model):
    nome = models.CharField("Categoria", max_length=20)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Categorias"
        ordering = ['nome']
    
class Metodo(models.Model):
    nome = models.CharField("Método", max_length=20)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Métodos"
        ordering = ['nome']

class Receita(models.Model):
    TIPOS = [
        ('VEGETARIANO', 'Vegetariano'),
        ('VEGANO', 'Vegano'),
        ('NENHUM', 'Nenhum'),
    ]
    ESTADOS = [
        ('PUBLICO', 'Público'),
        ('PRIVADO', 'Privado'),
    ]

    nome = models.CharField("Nome", max_length=200)
    categorias = models.ManyToManyField(Categoria, verbose_name="Categorias")
    metodos = models.ManyToManyField(Metodo, verbose_name="Metodos")
    tipo = models.CharField("Tipo", max_length=15, default="NENHUM", choices=TIPOS)
    porcoes = models.PositiveIntegerField("Porções")
    tempo_preparo = models.PositiveIntegerField("Tempo de preparo (minutos)", help_text="Informe o tempo total necessário em minutos")
    estado = models.CharField("Estado", max_length=10, default="PRIVADO", choices=ESTADOS)
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="receitas", verbose_name="Autor")
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Receitas"
        ordering = ['-criado_em']

class Ingrediente(models.Model):
    UNIDADES = [
        ('CAIXA', 'Caixa(s)'),
        ('COLHER_CHA', 'Colher(es) de chá'),
        ('COLHER_SOPA', 'Colher(es) de sopa'),
        ('GRAMA', 'Grama(s) / g(s)'),
        ('ML', 'Mililitro(s) / mL(s)'),
        ('UNIDADE', 'unidade(s)'),
        ('XICARA', 'Xicara(s)'),
    ]

    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name="ingredientes")
    nome = models.CharField("Nome", max_length=100)
    quantidade = models.PositiveIntegerField("Quantidade")
    unidade = models.CharField("Unidade", max_length=15, choices=UNIDADES)
    opcional = models.BooleanField("Opcional", default=False)

    def __str__(self):
        return f"{self.quantidade} {self.get_unidade_display()} de {self.nome}"
    
    class Meta:
        verbose_name_plural = "Ingredientes"

class Midia(models.Model):
    TIPOS_MIDIA = [
        ('IMAGEM', 'Imagem'),
        ('VIDEO', 'Video'),
    ]

    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name="midias")
    tipo = models.CharField("Tipo", max_length=10, choices=TIPOS_MIDIA)
    arquivo = models.FileField("Arquivo", upload_to="receitas/")

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.receita.nome}"
    
    class Meta:
        verbose_name_plural = "Mídias"

class Etapa(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name="preparo")
    conteudo = models.TextField("Conteudo")

    def __str__(self):
        return f"Etapa {self.id} da receita de {self.receita.nome}"
    
    class Meta:
        verbose_name_plural = "Preparo"
        ordering = ["id"]