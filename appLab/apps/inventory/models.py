from django.db import models
from apps.attendance.models import Students
from apps.store.models import Materials


class GivesItems(models.Model):
    mount = models.PositiveIntegerField("Cantidad")
    material = models.ForeignKey(Materials, on_delete=models.CASCADE, verbose_name="Materiales")

    class Meta():
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return f"Prestamo ID: {self.mount} - {self.material}"


class GivesTotal(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name="Estudiante")
    items = models.ManyToManyField(GivesItems, verbose_name="Items", blank=True)
    date_out = models.DateField('Fecha de prestamos', auto_now_add = True)
    date_back = models.DateField('Fecha de devolución')
    is_give = models.BooleanField('Entregado')
    is_back = models.BooleanField('Devuelto')
    observations = models.TextField('Observaciones', max_length=1024, null=True, blank= True)

    class Meta():
        verbose_name = "Prestamos"
        verbose_name_plural = "Prestamos"


    def __str__(self):
        return f"Prestamo ID: {self.id}"







