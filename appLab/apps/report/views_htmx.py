import pandas as pd
import plotly.express as px
from django.shortcuts import render
from apps.attendance.models import Students, TecnoEnabledResults, TopicEnabled
from django.db.models import Count, F, Q


# Vista para filtrar grupos por Nombre de estudiante
def ResultsFilterView(request):
    template_name = 'report/filterResultEnabled.html'
    class_name = request.GET.get('class_name')

    if len(class_name) <= 0 :
        context={
            'chart': None,
        }
    
        return render(request, template_name, context)
    
    students = Students.objects.filter(class_name__id = class_name)

    if students.count() <= 0:
        context={
            'chart': None,
        }

        return render(request, template_name, context)
    
    students_with_all_results_true = students.annotate(
        total_results=Count('student_enabled'),
        true_results=Count('student_enabled', filter=Q(student_enabled__status=True))
    ).filter(
        total_results=F('true_results')
    )   
    
    students_with_any_result_false = students.annotate(
        false_results=Count('student_enabled', filter=Q(student_enabled__status=False))
    ).filter(
        false_results__gt=0
    )   

    aprobe_students_count = students_with_all_results_true.count()
    reprobe_students_count = students_with_any_result_false.count()

    fig = px.pie(
        values=[aprobe_students_count, reprobe_students_count],
        names=['Aprobados', 'Reprobados'],
        title='Estado de habilitadores'
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    chart = fig.to_html()

    topics = TopicEnabled.objects.all()
    
    context = {
        'chart': chart,
        'topics': topics,
        'all_students': students,
        'aprobe_students': students_with_all_results_true,
        'reprobe_students': students_with_any_result_false
    }
    
    return render(request, template_name, context)