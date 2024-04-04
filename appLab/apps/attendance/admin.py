from django.contrib import admin
from django.utils.html import format_html
from import_export.resources import ModelResource, Field
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from .models import Attendance, Students, Classes, Teams, Schools, TecnoEnabledResults, TopicEnabled



# Resources
class AttendanceResource(ModelResource):
    class Meta:
        model = Attendance
        use_bulk = True
        batch_size = 500


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
    class_name = Field(column_name='class_name', attribute='class_name',widget=ManyToManyWidget(Classes, field='id', separator=','))

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
    list_display = ('name', 'display_class_name', 'display_class_name_year', 'display_class_name_stage', 'display_students')
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
    list_display = ('display_full_name', 'email', 'display_class_name', 'display_class_year', 'display_class_stage', 'display_team', 'display_tecno_enabled')
    list_filter = ('class_name__school__code', 'class_name__code')
    search_fields = ('name', 'last_name')
    filter_vertical = ('class_name',)

    @admin.display(description='Nombre completo')
    def display_full_name(self, obj):
        return f'{obj.name} {obj.last_name}'

    @admin.display(description='Asignatura')
    def display_class_name(self, obj):
        classes = obj.class_name.all()

        if classes:
            output = '<ul>'
            for class_name in classes:
                output += f'<li>{class_name.school.code} | {class_name.name}</li>'
            output += '</ul>'
            return format_html(output)
        else:
            return ''
        
    @admin.display(description='Año')
    def display_class_year(self, obj):
        classes = obj.class_name.all()

        if classes:
            output = '<ul>'
            for class_name in classes:
                output += f'<li>{class_name.year}</li>'
            output += '</ul>'
            return format_html(output)
        else:
            return ''
    
    @admin.display(description='Semestre')
    def display_class_stage(self, obj):
        classes = obj.class_name.all()

        if classes:
            output = '<ul>'
            for class_name in classes:
                output += f'<li>{class_name.get_stage_display()}</li>'
            output += '</ul>'
            return format_html(output)
        else:
            return ''

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
            return '❌'  
    
        for student in tecno_enabled:
            if not student.status:
                return '❌'  
    
        return '✅'  
       

    

@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    resource_class = AttendanceResource
    search_fields = ('student_student_name', 'student_student_last_name')
    list_display = ('display_student_name', 'date_in', 'time_inside')
    list_filter = ('student__class_name__year', 'student__class_name__stage', 'student__class_name__school__code')

    @admin.display(description='Estudiante')
    def display_student_name(self, obj):
        return f'{obj.student.name} {obj.student.last_name}'
    
   
@admin.register(TecnoEnabledResults)
class TecnoEnabledAdmin(admin.ModelAdmin):
    list_display = ('display_student_name', 'display_topic', 'display_score_result', 'status')
    readonly_fields = ('status', )


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
    list_display = ('name', 'score')

  

   

   



