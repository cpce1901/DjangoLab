from django.contrib import admin
from .models import Attendance, Students, Classses, Teams

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date_in']
    search_fields =['student__name', 'student__last_name']

    def student(self, obj):
        return obj

class StudentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'rut']
    search_fields = ['name', 'last_name']

    
admin.site.register(Classses)
admin.site.register(Teams)
admin.site.register(Students)
admin.site.register(Attendance, AttendanceAdmin)
ready