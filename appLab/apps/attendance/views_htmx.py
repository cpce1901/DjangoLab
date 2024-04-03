from django.shortcuts import render
from .models import Students, Teams


# Vista para filtrar grupos por Nombre de estudiante
def TeamsFilterView(request):
    teams, students = None, None
    name = request.GET.get('name')
    teams = Teams.objects.filter(team_name__name__icontains=name)
    if len(teams) == 0:
        students = Students.objects.filter(name__icontains=name)

    template_name = 'attendance/admin/filterTeams.html'
    context={
        'teams':teams,
        'students': students
        }
    
    return render(request, template_name, context)


# Vista para filtrar grupos por Nombre de estudiante
def StudentFilterView(request):
    name = request.GET.get('name')
    student = Students.objects.filter(name__icontains=name).first()
    
    template_name = 'attendance/admin/filterStudents.html'
    context={
        'student': student
        }

    return render(request, template_name, context)