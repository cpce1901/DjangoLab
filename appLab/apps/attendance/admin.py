from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ObjectDoesNotExist
from import_export.resources import ModelResource, Field
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from .models import Attendance, Students, Classes, Teams, Schools, TecnoEnabledResults, TopicEnabled
from datetime import datetime



# Resources
class TecnoEnabledResultResource(ModelResource):

    id = Field(column_name='ID')
    student = Field(column_name='Estudiante')
    sex = Field(column_name='Sexo')
    year = Field(column_name='Año')
    stage = Field(column_name='Semestre')
    school = Field(column_name='Escuela')
    class_name = Field(column_name='Asignatura')
    team = Field(column_name='Equipo')
    challenge = Field(column_name='Reto')
    topic = Field(column_name='Habilitador')
    score_result = Field(column_name='Puntaje')
    status = Field(column_name='Estado')

    class Meta:
        model = TecnoEnabledResults
        use_bulk = True
        batch_size = 500

    def dehydrate_id(self, obj):
        student_id = obj.id
        return f'{student_id}'

    def dehydrate_student(self, obj):
        student_name = getattr(obj.student, "name", "")
        student_last_name = getattr(obj.student, "last_name", "")
        return f'{student_name} {student_last_name}'
    
    def dehydrate_sex(self, obj):
        student_sex = getattr(obj.student, "sex", "")
        return f'{student_sex}'
    
    def dehydrate_year(self, obj):
        student_year = obj.student.class_name.year if obj.student.class_name else '-'
        return f'{student_year}'
    
    def dehydrate_stage(self, obj):
        student_stage = obj.student.class_name.get_stage_display() if obj.student.class_name else '-'
        return f'{student_stage}'
    
    def dehydrate_school(self, obj):
        student_school_name = obj.student.class_name.school.code if obj.student.class_name else '-'
        return f'{student_school_name}'
    
    def dehydrate_class_name(self, obj):
        student_class_name = getattr(obj.student.class_name, "name", "-")
        return f'{student_class_name}'
    
    def dehydrate_team(self, obj):
        if obj.student and obj.student.class_name:
            team = Teams.objects.filter(
                class_name=obj.student.class_name,
                team_name=obj.student
            ).first()
            
            if team:
                return f'{team.name}'
        
        return '-'
    
    def dehydrate_challenge(self, obj):
        if obj.student and obj.student.class_name:
            # Buscar el equipo al que pertenece el estudiante
            team = Teams.objects.filter(
                class_name=obj.student.class_name,
                team_name=obj.student
            ).first()
            
            if team and team.challenge:
                return f'{team.challenge}'
        
        return '-'
    
    def dehydrate_topic(self, obj):
        student_topic = obj.topic.name
        return f'{student_topic}'
    
    def dehydrate_score_result(self, obj):
        student_score = obj.score_result if obj.score_result else 'No realizado'
        return f'{student_score}'
    
    def dehydrate_status(self, obj):
        student_status = 'Habilitado' if obj.status else 'No habilitado'
        return f'{student_status}'


class AttendanceResource(ModelResource):

    id = Field(column_name='ID')
    student = Field(column_name='Estudiante')
    sex = Field(column_name='Sexo')
    email = Field(column_name='Email')
    year = Field(column_name='Año')
    stage = Field(column_name='Semestre')
    school = Field(column_name='Escuela')
    class_name = Field(column_name='Asignatura')
    team = Field(column_name='Equipo')
    date_in = Field(column_name='Hora de ingreso')
    time_inside = Field(column_name='Tiempo comprometido')

    class Meta:
        model = Attendance
        fields = ('id', 'student', 'sex', 'email', 'year', 'stage', 'school', 'class_name', 'team', 'date_in', 'time_inside')
        batch_size = 500

    
    def get_instance(self, instance_loader, row):
        try:
            return self.get_queryset().get(id=row['ID'])
        except Attendance.DoesNotExist:
            return None

    def import_obj(self, obj, data, dry_run, row_number=None, file_name=None, user=None):
        
    
        try:
            obj.student = Students.objects.get(email=data.get('Email'))
        except ObjectDoesNotExist:
            # Si el estudiante no existe, establecemos student como None
            obj.student = None
            # Opcionalmente, podrías registrar esto en un log o imprimir un mensaje
            print(f"Advertencia: No se encontró estudiante con email {data.get('Email')} en la fila {row_number}")
        
        obj.id = data.get('ID')
        obj.date_in = data.get('Hora de ingreso')
        obj.time_inside = data.get('Tiempo comprometido')
    
        return obj

    def skip_row(self, instance, original, row, import_validation_errors=None):
        if instance.student is None:
            return True
        return False

    def dehydrate_id(self, obj):
        student_id = obj.id
        return f'{student_id}'

    def dehydrate_student(self, obj):
        student_name = getattr(obj.student, "name", "")
        student_last_name = getattr(obj.student, "last_name", "")
        return f'{student_name} {student_last_name}'
    
    def dehydrate_sex(self, obj):
        student_sex = getattr(obj.student, "sex", "")
        return f'{student_sex}'
    
    def dehydrate_email(self, obj):
        student_year = obj.student.email if obj.student else '-'
        return f'{student_year}'
    
    def dehydrate_year(self, obj):
        if obj.student and obj.student.class_name:
            student_year = obj.student.class_name.year
        else:
            student_year = '-'
        return str(student_year)
    
    def dehydrate_stage(self, obj):
        if obj.student and obj.student.class_name:
            student_stage = obj.student.class_name.get_stage_display()
        else:
            student_stage = '-'
        return str(student_stage)

    def dehydrate_school(self, obj):
        if obj.student and obj.student.class_name and obj.student.class_name.school:
            student_school_name = obj.student.class_name.school.code
        else:
            student_school_name = '-'
        return str(student_school_name)

    def dehydrate_class_name(self, obj):
        if obj.student and obj.student.class_name:
            student_class_name = getattr(obj.student.class_name, "name", "-")
        else:
            student_class_name = "-"
        return str(student_class_name)
    
    def dehydrate_team(self, obj):
        if obj.student and obj.student.class_name:
            team = Teams.objects.filter(
                class_name=obj.student.class_name,
                team_name=obj.student
            ).first()
            
            if team:
                return f'{team.name}'
        
        return '-'
    
    def dehydrate_date_in(self, obj):
        student_date_in = obj.date_in or '-'
        if not student_date_in == '':
            return student_date_in
        return f'{student_date_in}'
    
    def dehydrate_time_inside(self, obj):
        student_time_inside = obj.time_inside or '-'
        return f'{student_time_inside}'


class ClassesResource(ModelResource):
    class Meta:
        model = Classes
        use_bulk = True
        batch_size = 500


class SchoolsResource(ModelResource):
    class Meta:
        model = Schools
        use_bulk = True
        batch_size = 500


class StudentsResource(ModelResource):
    class_name = Field(column_name='class_name', attribute='class_name',widget=ForeignKeyWidget(Classes, field='id'))

    class Meta:
        model = Students
        se_bulk = True
        batch_size = 500


class TeamsResource(ModelResource):   
    team_name = Field(column_name='team_name', attribute='team_name',widget=ManyToManyWidget(Students, field='id', separator=','))

    def before_import_row(self, row, **kwargs):
        team_id = row['id']
        team_ids = [int(sid) for sid in row.get("team_name", "").split(",") if sid.strip()]
        instance, created = Teams.objects.get_or_create(id=team_id, defaults={'id': team_id})
        if created:
            instance.team_name.add(*team_ids)

    class Meta:
        model = Teams
        batch_size = 500
      

# Inlines
class ClassesIline(admin.TabularInline):
    model = Classes
    extra = 0


class TeamsInline(admin.TabularInline):
    filter_vertical = ('team_name',)
    model = Teams
    extra = 0


class StudentInline(admin.TabularInline):
    model = Students
    extra = 0


class TecnoEnabledResultInline(admin.TabularInline):
    model = TecnoEnabledResults
    extra = 0


# ModelAdmin by Models
    
@admin.register(Schools)
class SchoolsAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    '''
    Administyración carrera
    
    '''

    resource_class = SchoolsResource
    list_display = ('sede_code', 'code', 'name')
    inlines = (ClassesIline,)
    

@admin.register(Classes)
class ClassesAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    '''
    Administyración asignaturas
    
    '''

    resource_class = ClassesResource
    inlines = (TeamsInline, )
    list_display = ('display_school_code', 'stage', 'year', 'code', 'name', 'teacher', 'display_teams')
    list_filter = ('year', 'stage', 'school__code')

    @admin.display(description='Escuela')
    def display_school_code(self, obj):
        return obj.school.code
    
    @admin.display(description='Escuela')
    def display_school(self, obj):
        return obj.school.name
    
    @admin.display(description='Grupos')
    def display_teams(self, obj):
        teams = obj.class_team.all()

        if teams:
            output = '<ul>'
            for team in teams:
                output += f'<li>{team.name}</li>'
            output += '</ul>'
            return format_html(output)
        else:
            return ''
    
    
@admin.register(Teams)
class TeamsAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    resource_class = TeamsResource    
    list_display = ('name', 'display_class_name', 'display_class_name_year', 'display_class_name_stage', 'display_students', 'challenge')
    list_filter = ('class_name__school__code', 'class_name__year', 'class_name__stage')
    filter_vertical = ('team_name',)

    @admin.display(description='Asignatura')
    def display_class_name(self, obj):
        return f'{obj.class_name.school.code} | {obj.class_name.name}'
    
    @admin.display(description='Año')
    def display_class_name_year(self, obj):
        return obj.class_name.year
    
    @admin.display(description='Semestre')
    def display_class_name_stage(self, obj):
        return obj.class_name.get_stage_display()
    
    @admin.display(description='Integrantes')
    def display_students(self, obj):
        students = obj.team_name.all()
        
        if students:
            output = '<ul>'
            for student in students:
                output += f'<li>{student.name} {student.last_name}</li>'
            output += '</ul>'
            return format_html(output)
        else:
            return ''
   

@admin.register(Students) 
class StudentsAdmin(ImportExportModelAdmin, ExportActionModelAdmin): 
    resource_class = StudentsResource
    inlines = (TecnoEnabledResultInline,)
    list_display = ('display_full_name', 'sex', 'email', 'display_class_name', 'display_class_year', 'display_class_stage', 'display_team', 'display_tecno_enabled')
    list_filter = ('class_name__school__code', 'class_name__code')
    search_fields = ('name', 'last_name', 'email')

    @admin.display(description='Nombre completo')
    def display_full_name(self, obj):
        return f'{obj.name} {obj.last_name}'

    @admin.display(description='Asignatura')
    def display_class_name(self, obj):
        return f"{obj.class_name.name if obj.class_name else '-'}"
        
    @admin.display(description='Año')
    def display_class_year(self, obj):
        return f"{obj.class_name.year if obj.class_name else '-'}"
    
    @admin.display(description='Semestre')
    def display_class_stage(self, obj):
        return f"{obj.class_name.get_stage_display() if obj.class_name else '-'}"

    @admin.display(description='Grupo')
    def display_team(self, obj):
        teams = obj.team_student.all()

        if teams:
            output = '<ul>'
            for team in teams:
                output += f'<li>{team.name}</li>'
            output += '</ul>'
            return format_html(output)
        else:
            return ''
        
    @admin.display(description='Todo habilitado')
    def display_tecno_enabled(self, obj):
        tecno_enabled = obj.student_enabled.all()

        if not tecno_enabled:
            return '❔'  
    
        for student in tecno_enabled:
            if not student.status:
                return '❌'  
    
        return '✅'  
       

@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    resource_class = AttendanceResource
    search_fields = ('student__name', 'student__last_name')
    list_display = ('display_student_name', 'date_in', 'time_inside')
    list_filter = ('student__class_name__year', 'student__class_name__stage', 'student__class_name__school__code')

    @admin.display(description='Estudiante')
    def display_student_name(self, obj):
        return f'{obj.student.name if obj.student else ""} {obj.student.last_name if obj.student else ""}'
    
   
@admin.register(TecnoEnabledResults)
class TecnoEnabledAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    resource_class = TecnoEnabledResultResource
    list_display = ('display_student_name', 'display_topic', 'display_score_result', 'status')
    readonly_fields = ('status', )
    list_filter = ('student__class_name__school__code', 'student__class_name__code')


    @admin.display(description='Estudiante')
    def display_student_name(self, obj):
        return f'{obj.student.name if obj.student else None} {obj.student.last_name if obj.student else None}'
    
    @admin.display(description='Habilitador')
    def display_topic(self, obj):
        return f'{obj.topic.name}'
    
    @admin.display(description='Resultado')
    def display_score_result(self, obj):
        return f'{obj.score_result if obj.score_result else 0}/{obj.topic.score}'


@admin.register(TopicEnabled)
class TecnoEnabledAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'score')
    ordering = ('id', )

  

   

   



