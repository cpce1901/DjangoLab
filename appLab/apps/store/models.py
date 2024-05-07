from typing import Any
from django.db import models
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from apps.attendance.models import Students


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
        return f"{self.description} | <{self.stock}>"
    
    def save(self, *args, **kwargs):
        self.enabled = self.stock > 0
        super().save(*args, **kwargs)


class Gives(models.Model):
    student  = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='Estudiante')
    date_out = models.DateField('Fecha de prestamo', auto_now_add = True)
    date_back = models.DateField('Fecha de devolución')
    observations = models.TextField('Observaciones', max_length=1024, null=True, blank= True)

    class Meta():
        verbose_name = "Prestamos"
        verbose_name_plural = "Prestamos"

    def __str__(self):
        return f"Prestamo: {self.student.name} - {self.date_out}"
    

        
class Items(models.Model):
    gives = models.ForeignKey(Gives, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Prestamo', related_name='items_gives_gives')
    item = models.ForeignKey(Materials, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Items', related_name='items_gives_item')
    count = models.SmallIntegerField('Cantidad', default=0)
    count_save = models.SmallIntegerField('Cantidad guardada', default=0)
    is_back = models.BooleanField('Devuelto', default=False)

    class Meta():
        verbose_name = "Item"
        verbose_name_plural = "Items"
        unique_together = ('gives', 'item')

    def __str__(self):
        return f"Item ID: {self.id}"
    

    def save(self, *args, **kwargs):
        if self.count_save > self.count:
            return

        if self.is_back:
            self.item.stock += self.count
            self.item.save()
        else:
            self.item.stock -= self.count
            self.item.save()

        self.count_save = self.count
        self.count = 0
        super().save(*args, **kwargs)
     
            

    
    
    

      
    
    
    