from django.db import models


class Students(models.Model):
    name = models.CharField('Nombre', max_length=32)
    last_name = models.CharField('Apellido', max_length=32)
    rut = models.CharField('RUT', max_length=10)


    class Meta():
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Schools(models.Model):
    name = models.CharField('Carrera', max_length=64)

    class Meta():
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"

    def __str__(self):
        return f"{self.name}"


class Classes(models.Model):
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, verbose_name='Carrera', related_name='school')
    name = models.CharField('Asignatura', max_length=64)
    code = models.CharField('Codigo', max_length=16)
    teacher = models.CharField('Profesor', max_length=32)

    class Meta():
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"

    def __str__(self):
        return f"{self.name} {self.teacher}"
    

class Teams(models.Model):
    name = models.CharField('Nombre', max_length=32)
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE, verbose_name='Asignatura', related_name='class_name')
    students = models.ManyToManyField(Students, verbose_name="Estudiantes", blank=True)
    
    class Meta():
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        

    def __str__(self):
        return f"{self.name}"


class Attendance(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='Estudiante')
    date_in = models.DateTimeField('Ingreso', auto_now_add = True)
    time_inside = models.TimeField('Tiempo estimado de permanencia')

    class Meta():
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"

    def __str__(self):
        return f"{self.date_in}"