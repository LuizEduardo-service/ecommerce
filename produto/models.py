from django.db import models
from PIL import Image
import os
from django.conf import settings
# Create your models here.

"""    
    Variacao:
        nome - char
        produto - FK Produto
        preco - Float
        preco_promocional - Float
        estoque - Int"""

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(default='V', max_length=1, choices=(('V', 'Variação'), ('S', 'Simples')))

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size
        new_height = round(new_width * original_height) / original_width


        if original_width <= new_width:
            img_pil.close()

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

        print(img.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image_size = 800
        if self.imagem:
            self.resize_image(self.imagem, image_size)


    def __str__(self):
        return self.nome


class Variacao(models.Model):

    nome = models.CharField(max_length=100, blank=True, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'