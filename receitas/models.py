from django.db import models

class Categoria(models.Model):
    nome = models.CharField("Categoria", max_length=20)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Categorias"
    
class Metodo(models.Model):
    nome = models.CharField("Método", max_length=20)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Métodos"
    
TIPOS = [
        ('VEGETARIANO', 'Vegetariano'),
        ('VEGANO', 'Vegano'),
        ('NENHUM', 'Nenhum'),
    ]

class Receita(models.Model):
    nome = models.CharField("Nome", max_length=200)
    categorias = models.ManyToManyField(Categoria, verbose_name="Categorias")
    metodos = models.ManyToManyField(Metodo, verbose_name="Metodos")
    tipo = models.CharField("Tipo", max_length=15, choices=TIPOS)
    porcoes = models.PositiveIntegerField("Porções")
    tempo_preparo = models.PositiveIntegerField("Tempo de preparo (minutos)", help_text="Informe o tempo total necessário em minutos")
    preparo = models.TextField("Preparo")
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Receitas"
        ordering = ['-criado_em']

UNIDADES = [
        ('ML', 'mls'),
        ('XICARA', 'Xicaras'),
        ('COLHER_SOPA', 'Colheres de sopa'),
        ('UNIDADE', 'unidades'),
        ('COLHER_CHA', 'Colheres de chá'),
        ('GRAMA', 'Gramas')
    ]

class Ingrediente(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name="ingredientes")
    nome = models.CharField("Nome", max_length=100)
    quantidade = models.PositiveIntegerField("Quantidade")
    unidade = models.CharField("Unidade", max_length=15, choices=UNIDADES)

    def __str__(self):
        return f"{self.quantidade} {self.get_unidade_display()} de {self.nome}"
    
    class Meta:
        verbose_name_plural = "Ingredientes"