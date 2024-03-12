from django.contrib import admin
from django.utils.html import format_html
from import_export.resources import ModelResource
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from .models import Attendance, Students, Classes, Teams, Schools
from .models import Students, Teams, Classes

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
    class Meta:
        model = Students
        use_bulk = True
        batch_size = 500


class TeamsResource(ModelResource):
    class Meta:
        model = Teams
        use_bulk = True
        batch_size = 500


# Inlines
class ClassesIline(admin.TabularInline):
    model = Classes
    extra = 0


class TeamsInline(admin.TabularInline):
    model = Teams
    extra = 0


class StudentInline(admin.TabularInline):
    model = Students
    extra = 0


# ModelAdmin by Models
@admin.register(Teams)
class TeamsAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    resource_class = TeamsResource    
    list_display = ('name', 'get_class', 'get_year', 'get_stage', 'get_students') 
    search_fields = ('class_name__name', 'class_name__year', 'class_name__stage')

    def get_students(self, obj):
        students = obj.team.all()
        if students:
            output = "<ul>"
            for student in students:
                output += f"<li>{student.name}</li>"
            output += "</ul>"
            return format_html(output)
        else:
            return "No hay alumnos asociados"
        
    def get_class(self, obj):
        class_name = obj.class_name.name if obj.class_name else None
        return class_name
    
    def get_year(self, obj):
        class_year = obj.class_name.year if obj.class_name else None
        return class_year
    
    def get_stage(self, obj):
        class_stage = obj.class_name.get_stage_display() if obj.class_name else None
        return f'{class_stage} Semestre'
    
    get_class.short_description = "Asignatura"
    get_year.short_description = "Año"
    get_stage.short_description = "Semestre"
    get_students.short_description = 'Integrantes'


@admin.register(Students) 
class StudentsAdmin(ImportExportModelAdmin, ExportActionModelAdmin): 
    resource_class = StudentsResource
    list_display = ('name', 'last_name', 'rut', 'email', 'display_class', 'display_year', 'display_stage', 'display_team')
    search_fields = ['name', 'last_name', 'team__class_name__year']
    autocomplete_fields = ["team"]

    @admin.display(description='Grupo')
    def display_team(self, obj):
        team = obj.team
        return team.name
    
    @admin.display(description='Asignatura')
    def display_class(self, obj):
        class_student = obj.team.class_name 
        return class_student.name
    
    @admin.display(description='Año')
    def display_year(self, obj):
        class_student = obj.team.class_name 
        return class_student.year
    
    @admin.display(description='Semestre')
    def display_stage(self, obj):
        class_student = obj.team.class_name 
        return class_student.get_stage_display()
    
   
@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    resource_class = AttendanceResource
    list_display = ['student', 'date_in', 'time_inside']
    search_fields =['student__name', 'student__last_name']

    def student(self, obj):
        return obj


@admin.register(Classes)
class ClassesAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    '''
    Administyración asignaturas
    
    '''

    resource_class = ClassesResource
    list_display = ('year', 'stage', 'school', 'code', 'name', 'teacher', 'display_teams')
    search_fields = ('school__name', 'year')
    list_filter = ('year', 'stage', 'code')
    inlines = (TeamsInline, )

    def display_teams(self, obj):
        teams = obj.class_name.all()
        if teams:
            output = "<ul>"
            for team in teams:
                output += f"<li>{team.name}</li>"
            output += "</ul>"
            return format_html(output)
        else:
            return "No hay equipos asociados"
        
    display_teams.short_description = 'Equipos'


@admin.register(Schools)
class SchoolsAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    '''
    Administyración carrera
    
    '''

    resource_class = SchoolsResource
    list_display = ('sede_code', 'code', 'name')
    inlines = (ClassesIline,)
    
    


