from django.db import models
from datetime import datetime


class Classses(models.Model):
    name = models.CharField('Nombre', max_length=32)
    teacher = models.CharField('Profesor', max_length=32)

    class Meta():
        verbose_name = "Clase"
        verbose_name_plural = "Clases"

    def __str__(self):
        return f"{self.name} {self.teacher}"
    

class Teams(models.Model):
    name = models.CharField('Nombre', max_length=32)
    clase = models.ForeignKey(Classses, on_delete=models.CASCADE, verbose_name='Clase')


    class Meta():
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

    def __str__(self):
        return f"{self.name}"



class Students(models.Model):
    name = models.CharField('Nombre', max_length=32)
    last_name = models.CharField('Apellido', max_length=32)
    rut = models.CharField('RUT', max_length=10)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, verbose_name='Equipo')

    class Meta():
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self):
        return f"{self.name} {self.last_name}"



class Attendance(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='Estudiante')
    date_in = models.DateTimeField('Fecha', auto_now_add = True)
    time_inside = models.TimeField('Tiempo estimado de permanencia')

    class Meta():
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"

    def __str__(self):
        return f"{self.date_in}"