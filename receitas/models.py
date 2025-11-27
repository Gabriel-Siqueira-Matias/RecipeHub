from django.db import models
from usuarios.models import Perfil
from django.core.validators import MinValueValidator

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
    class Tipos(models.TextChoices):
        VEGETARIANO = 'VEGETARIANO', 'Vegetariano'
        VEGANO = 'VEGANO', 'Vegano'
        NENHUM = 'NENHUM', 'Nenhum'
    class Estados(models.TextChoices):
        PUBLICO = 'PUBLICO', 'Público'
        PRIVADO = 'PRIVADO', 'Privado'

    nome = models.CharField("Nome", max_length=200)
    categorias = models.ManyToManyField(Categoria, related_name="receitas_categoria", verbose_name="Categorias")
    metodos = models.ManyToManyField(Metodo, related_name="receitas_metodo", verbose_name="Metodos")
    tipo = models.CharField("Tipo", max_length=15, default=Tipos.NENHUM, choices=Tipos.choices)
    porcoes = models.PositiveIntegerField("Porções")
    tempo_preparo = models.PositiveIntegerField("Tempo de preparo (minutos)", help_text="Informe o tempo total necessário em minutos")
    estado = models.CharField("Estado", max_length=10, default=Estados.PRIVADO, choices=Estados.choices)
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="receitas_autor", verbose_name="Autor")
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"
        ordering = ['-criado_em']

class Ingrediente(models.Model):
    class Unidades(models.TextChoices):
        CAIXA = 'CAIXA', 'caixa(s)'
        COLHER_CHA = 'COLHER_CHA', 'colher(es) de chá'
        COLHER_SOPA = 'COLHER_SOPA', 'colher(es) de sopa'
        COPO = 'COPO', 'copo(s)'
        GRAMA = 'GRAMA', 'grama(s) / g(s)'
        LATA = 'LATA', 'lata(s)'
        MILILITRO = 'MILILITRO', 'mililitro(s) / mL(s)'
        UNIDADE = 'UNIDADE', 'unidade(s)'
        XICARA = 'XICARA', 'xicara(s)'

    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name="ingredientes")
    nome = models.CharField("Nome", max_length=100)
    quantidade = models.FloatField("Quantidade", validators=[MinValueValidator(0.0)])
    unidade = models.CharField("Unidade", max_length=15, choices=Unidades.choices)
    opcional = models.BooleanField("Opcional", default=False)

    def __str__(self):
        return f"{self.quantidade} {self.get_unidade_display()} de {self.nome}"
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantidade__gte=0.0),
                name='quantidade_positiva_ingrediente'
            )
        ]
        verbose_name_plural = "Ingredientes"

class Midia(models.Model):
    class Tipos_Midia(models.TextChoices):
        IMAGEM = 'IMAGEM', 'Imagem'
        VIDEO = 'VIDEO', 'Video'

    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name="midias")
    tipo = models.CharField("Tipo", max_length=10, choices=Tipos_Midia.choices)
    arquivo = models.FileField("Arquivo", upload_to="receitas/", max_length=500)

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.receita.nome}"
    
    class Meta:
        verbose_name_plural = "Mídias"

class Etapa(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name="etapas")
    conteudo = models.TextField("Conteudo")

    def __str__(self):
        return f"Etapa {self.id} da receita de {self.receita.nome}"
    
    class Meta:
        verbose_name_plural = "Etapas"
        ordering = ["id"]