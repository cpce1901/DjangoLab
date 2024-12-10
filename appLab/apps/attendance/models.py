from django.db import models
from django.db import transaction


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
    class_name = models.ForeignKey(Classes, on_delete=models.SET_NULL, verbose_name='Asignatura', related_name='class_student', null=True, blank=True)
    sex = models.CharField('Sexo', max_length=16, null=False, blank=False, default='Hombre')
    rut = models.CharField('rut', max_length=10, null=True, blank=True, unique=True)
    score = models.FloatField('Nota', blank=True, null=True)
    
    
    class Meta():
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        unique_together= ['name', 'last_name', 'email']

    def __str__(self):
        return f"{self.name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Sobrescribimos el método save para asignar tecnologías automáticamente.
        creating = self.pk is None  # Verificamos si el estudiante se está creando (nuevo objeto)
        super(Students, self).save(*args, **kwargs)

        if creating:
            # Asignamos todas las tecnologías con un puntaje inicial de 0
            from .models import TopicEnabled, TecnoEnabledResults

            # Garantizamos que la operación sea atómica
            with transaction.atomic():
                tecnologias = TopicEnabled.objects.all()
                resultados = [
                    TecnoEnabledResults(student=self, topic=tecnologia, score_result=0, status=False)
                    for tecnologia in tecnologias
                ]
                TecnoEnabledResults.objects.bulk_create(resultados)


class Technology(models.Model):
    name = models.CharField('Nombre', max_length=32)

    class Meta():
        verbose_name = "Tecnologia"
        verbose_name_plural = "Tecnologias"

    def save(self, *args, **kwargs):
        self.name = self.name.upper()

        super(Technology, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class TopicEnabled(models.Model):
    name = models.CharField('Nombre', max_length=32)
    technology = models.ForeignKey(Technology, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.SmallIntegerField('Puntaje', null=True, blank=True)

    class Meta():
        verbose_name = "Tipo Habilitador"
        verbose_name_plural = "Tipos Habilitador"

    def save(self, *args, **kwargs):
        self.name = self.name.upper()

        super(TopicEnabled, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class TecnoEnabledResults(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='Estudiante', related_name='student_enabled', null=True, blank=True)
    topic = models.ForeignKey(TopicEnabled, on_delete=models.SET_NULL, verbose_name='Nombre habilitador', related_name='topic_enabled', null=True, blank=True)
    score_result = models.SmallIntegerField('Puntaje obtenido', null=True, blank=True)
    status = models.BooleanField('Estado')
    
    class Meta():
        verbose_name = "Resultado Habilitadores"
        verbose_name_plural = "Resultados Habilitadores"
        unique_together = ['student', 'topic']


    def save(self, *args, **kwargs):
        if self.score_result is not None:
            if self.score_result >= 60:
                self.status = True
        else:
            self.status = False

        super(TecnoEnabledResults, self).save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.topic.name} {self.score_result} {self.status}"


class Teams(models.Model):
    name = models.CharField('Nombre', max_length=32)
    challenge = models.CharField('Reto', max_length=128, null=True, blank=True)
    technology = models.ForeignKey(Technology, on_delete=models.SET_NULL, null=True, blank=True)
    class_name = models.ForeignKey(Classes, on_delete=models.SET_NULL, verbose_name='Asignatura', related_name='class_team', null=True, blank=True)
    team_name = models.ManyToManyField(Students, verbose_name='Equipo', related_name='team_student', blank=True)
    details = models.TextField('Observaciones', null=True, blank=True)
    file = models.FileField('Informe', upload_to='documents/', null=True, blank=True)
    

    class Meta():
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

    def save(self, *args, **kwargs):
        self.details = self.details.upper()
        super(Teams, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name} | {self.class_name.name} | {self.class_name.year}"


class Attendance(models.Model):
    
    '''
    Modelo de asistencia, incluye ingreso y tiempo de permanencia

    '''

    student = models.ForeignKey(Students, on_delete=models.SET_NULL, verbose_name='Estudiante', null=True)
    date_in = models.DateTimeField('Ingreso', auto_now_add = True)
    time_inside = models.TimeField('Tiempo estimado de permanencia')

    class Meta():
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"

    def __str__(self):
        return f"{self.date_in}"