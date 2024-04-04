from django.shortcuts import render
from .models import Students, Teams, TecnoEnabledResults
from django.db.models import Case, When, Value, BooleanField, Exists, OuterRef


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
    input_email = request.GET.get('email', '').strip()

    students = Students.objects.filter(email__icontains=input_email).annotate(
        has_results=Exists(TecnoEnabledResults.objects.filter(student=OuterRef('pk'))),
        status_all=Case(
            When(has_results=True, then=Case(
                When(~Exists(TecnoEnabledResults.objects.filter(student=OuterRef('pk'), status=False)), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )),
            default=Value(None),
            output_field=BooleanField(null=True)
        )
    )

    template_name = 'attendance/admin/filterStudents.html'
    context = {
        'students': students
    }

    return render(request, template_name, context)