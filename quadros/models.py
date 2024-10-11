# quadros/models.py

from django.db import models

class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
        
class Pictures(models.Model):  # Tabela no banco de dados
    id = models.AutoField(primary_key=True)  # Auto incremento
    model = models.CharField(max_length=300)  # Modelo do quadro - campo de texto
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, related_name='pictures_artist')  # Autor do quadro/o campo vai ser uma ligação com a tabela ARTIST
    factory_year = models.IntegerField(blank=True, null=True)  # Ano do quadro
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Valor do quadro
    photo = models.ImageField(upload_to='quadros/', blank=True, null=True) # Imagem
    bio = models.TextField(blank=True, null=True)  # Descrição do quadro
    artistic_style = models.CharField(max_length=4, choices=[
        ('REN', 'Renascimento'),
        ('BAR', 'Barroco'),
        ('ROC', 'Rococó'),
        ('NEO', 'Neoclassicismo'),
        ('ROM', 'Romantismo'),
        ('REA', 'Realismo'),
        ('IMP', 'Impressionismo'),
        ('POS', 'Pós-Impressionismo'),
        ('EXP', 'Expressionismo'),
        ('CUB', 'Cubismo'),
        ('FUT', 'Futurismo'),
        ('SUR', 'Surrealismo'),
        ('ABS', 'Abstracionismo'),
        ('POP', 'Pop Art'),
        ('MIN', 'Minimalismo'),
        ('CONT', 'Arte Contemporânea'),
        ('DIG', 'Arte Digital'),
        ('URB', 'Arte Urbana'),
        ('CONC', 'Arte Conceitual'),
        ('NOUV', 'Arte Nouveau'),
        ('DECO', 'Arte Déco'),
    ], default='REN')  # Estilo artístico

    def __str__(self):
        return self.model


class PicturesInventory(models.Model):
    pic_count = models.IntegerField()  
    pic_value = models.FloatField()  # quantos esta valendo em dinheiro nosso estoque
    created_at = models.DateTimeField(auto_now_add=True)  # amarzena data e horario

    class Meta:
        ordering = ['-created_at']  # ordenar o campo de forma decrescente

    def __str__(self):
        return f"{self.pic_count} quadros, totalizando R$ {self.pic_value}"
