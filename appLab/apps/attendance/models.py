from django.db import models


class Schools(models.Model):

    '''
    Modelo de carrera, incluye nombre de la carrea, su codigo y el codigo de sede

    '''

    SEDE_CODE_CHOICES = [
        ('0', 'BES' ), # Bellavista Santiago
        ('1', 'TPC'), # Tres pascualas Concepcion
        ('2', 'PAP') # Puerto Mont
    ]

    name = models.CharField('Carrera', max_length=64)
    code = models.CharField('Codigo', max_length=8)
    sede_code = models.CharField('Codigo de sede', max_length=1, choices=SEDE_CODE_CHOICES)

    class Meta():
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"

    def __str__(self):
        return f"{self.name}"


class Classes(models.Model):

    '''
    Modelo de asignaturas para cada carrera, incliuye año, semestre

    '''

    STAGE_CHOICES = [
        ('0', '1°'),
        ('1', '2°')
    ]

    name = models.CharField('Asignatura', max_length=64)
    code = models.CharField('Codigo', max_length=16)
    year = models.IntegerField('Año')
    stage = models.CharField('Semestre', max_length=1, choices=STAGE_CHOICES)
    teacher = models.CharField('Profesor', max_length=32, null=True, blank=True)
    school = models.ForeignKey(Schools, on_delete=models.SET_NULL, verbose_name='Carrera', related_name='school', null=True, blank=True)

    class Meta():
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"

    def __str__(self):
        return f"{self.school.code} | {self.name} | {self.get_stage_display()} Semestre | {self.year}"


class Students(models.Model):

    '''
    Modelo de estudiante

    '''
     
    name = models.CharField('Nombre', max_length=32)
    last_name = models.CharField('Apellido', max_length=32)
    email = models.EmailField('Email', null=True)
    class_name = models.ManyToManyField(Classes, verbose_name='Asignatura', related_name='class_student', blank=True)
    
    class Meta():
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        unique_together= ['name', 'last_name', 'email']

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Teams(models.Model):
    name = models.CharField('Nombre', max_length=32)
    challenge = models.CharField('Reto', max_length=32, null=True, blank=True)
    class_name = models.ForeignKey(Classes, on_delete=models.SET_NULL, verbose_name='Asignatura', related_name='class_team', null=True, blank=True)
    team_name = models.ManyToManyField(Students, verbose_name='Equipo', related_name='team_student', blank=True)

    class Meta():
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        
    def __str__(self):
        return f"{self.name} | {self.class_name.name} | {self.class_name.year}"


class Attendance(models.Model):
    
    '''
    Modelo de asistencia, incluye ingreso y tiempo de permanencia

    '''

    student = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='Estudiante')
    date_in = models.DateTimeField('Ingreso', auto_now_add = True)
    time_inside = models.TimeField('Tiempo estimado de permanencia')

    class Meta():
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"

    def __str__(self):
        return f"{self.date_in}"