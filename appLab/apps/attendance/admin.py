from django.contrib import admin
from django.utils.html import format_html
from import_export.resources import ModelResource
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from .models import Attendance, Students, Classes, Teams, Schools
from .models import Students, Teams, Classes
from django.db.models import Q

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
    filter_vertical = ('students',)
    model = Teams
    extra = 0


class StudentInline(admin.TabularInline):
    model = Students
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
    list_display = ('display_school_code', 'stage', 'year', 'code', 'name', 'teacher', 'display_teams')
    search_fields = ('school__name', 'year')
    list_filter = ('year', 'stage', 'code')
    inlines = (TeamsInline, )

    @admin.display(description='Codigo')
    def display_school_code(self, obj):
        return obj.school.code

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




@admin.register(Teams)
class TeamsAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    resource_class = TeamsResource    
    list_display = ('name', 'get_class', 'get_year', 'get_stage', 'get_students') 
    filter_horizontal = ('students', )
    search_fields = ('name', 'class_name__name', 'class_name__year')

    def get_students(self, obj):
        students = obj.students.all()
        if students:
            output = "<ul>"
            for student in students:
                output += f"<li>{student.name} { student.last_name }</li>"
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
    list_display = ('display_full_name', 'id', 'rut', 'email', 'display_class', 'display_year', 'display_stage', 'display_team')
    search_fields = ('name', 'last_name', 'team__class_name__year')
    ordering = ('name', )
   
    @admin.display(description='Nombre completo')
    def display_full_name(self, obj):
        if obj:
            return f'{obj.name} {obj.last_name}'
        return '-'
    
    @admin.display(description='Grupo')
    def display_team(self, obj):
        equipos_del_estudiante = obj.teams_set.all()
        nombres_asignaturas = []
        for equipo in equipos_del_estudiante:
            nombres_asignaturas.append(equipo.name)
        return ", ".join(nombres_asignaturas)
    

    @admin.display(description='Asignatura')
    def display_class(self, obj):
        equipos_del_estudiante = obj.teams_set.all()
        nombres_asignaturas = []
        for equipo in equipos_del_estudiante:
            nombres_asignaturas.append(equipo.class_name.name)
        return ", ".join(nombres_asignaturas)
        
    
    @admin.display(description='Año')
    def display_year(self, obj):
        equipos_del_estudiante = obj.teams_set.all()
        print(equipos_del_estudiante)
        nombres_asignaturas = []
        for equipo in equipos_del_estudiante:
            nombres_asignaturas.append(str(equipo.class_name.year))
        return ", ".join(nombres_asignaturas)
        
    
    @admin.display(description='Semestre')
    def display_stage(self, obj):
        equipos_del_estudiante = obj.teams_set.all()
        nombres_asignaturas = []
        for equipo in equipos_del_estudiante:
            nombres_asignaturas.append(equipo.class_name.get_stage_display())
        return ", ".join(nombres_asignaturas)
       


@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    resource_class = AttendanceResource
    list_display = ['student', 'date_in', 'time_inside']
    search_fields =['student__name', 'student__last_name']

    def student(self, obj):
        return obj

   



