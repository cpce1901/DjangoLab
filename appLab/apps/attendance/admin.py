from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from .models import Attendance, Students, Classes, Teams, Schools


# Inlines
class ClassesIline(admin.TabularInline):
    model = Classes
    extra = 0

class TeamsInline(admin.TabularInline):
    filter_horizontal = ['students',]
    model = Teams
    extra = 0

class StudentInline(admin.TabularInline):
    model = Students
    extra = 0

# ModelAdmin by Models
    

class ClassesAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_teams']
    inlines = [TeamsInline, ]

    def get_teams(self, obj):
        all_teams = obj.class_name.all()
        teams = [f"<li>{team.name}</li>" for team in all_teams]

        if teams:
            teams_html = "<ul>" + "".join(teams) + "</ul>"
            return format_html(teams_html)
        else:
            teams_html = "<ul>" + "<li>No existen equipos en esta asignatura......</li>" + "</ul>"
            return format_html(teams_html)



class TeamsAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_class', 'get_teams'] 
    filter_horizontal = ['students',]

    def get_class(self, obj):
        class_name = obj.class_name.name if obj.class_name else None
        return class_name
    
    def get_teams(self, obj):
        team = obj.students.all()
        students = [f"<li>{student.name}</li>" for student in team]

        if students:
            students_html = "<ul>" + "".join(students) + "</ul>"
            return format_html(students_html)
        else:
            students_html = "<ul>" + "<li>No existen estudiantes en este grupo...</li>" + "</ul>"
            return format_html(students_html)
 
    
    get_class.short_description = "Asignatura"
    get_teams.short_description = "Grupo de trabajo"
 
    
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date_in']
    search_fields =['student__name', 'student__last_name']

    def student(self, obj):
        return obj


class StudentsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'rut', 'get_class', 'get_team']
    search_fields = ['name', 'last_name']

   
    def full_name(self, obj):
        return f"{obj.name} {obj.last_name}"
    
    def get_class(self, obj):
        # Obtiene la clase correspondiente al estudiante
        class_name = obj.teams_set.first().class_name if obj.teams_set.exists() else None
        return class_name.name if class_name else None
    
    def get_team(self, obj):
        team_name = obj.teams_set.first() if obj.teams_set.exists() else None
        return team_name.name if team_name else None
 
           
    full_name.short_description = "Nombre"
    get_class.short_description = "Asignatura"
    get_team.short_description = "Equipo"
 
    
    
    
    
admin.site.register(Schools)
admin.site.register(Classes, ClassesAdmin)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(Students, StudentsAdmin)
admin.site.register(Attendance, AttendanceAdmin)
