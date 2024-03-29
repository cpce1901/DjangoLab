from django.db import models

# Create your models here.
class Categories(models.Model):
    name = models.CharField('Categoria', max_length=64)

    class Meta():
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return f"{self.name}"
    
    
class Materials(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, verbose_name='Categoria', null=True, blank=True)
    code = models.CharField('Code', max_length=32, unique=True)
    item = models.CharField('Item', max_length=128, unique=True)
    description = models.CharField('Description', max_length=512)
    stock = models.SmallIntegerField('Stock')
    enabled = models.BooleanField('Disponible', default=True)
    details = models.CharField('Detalles', max_length=128, null=True, blank=True)

    class Meta():
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        unique_together= ['category', 'code', 'item', 'description']

    def __str__(self):
        return f"{self.description}"
