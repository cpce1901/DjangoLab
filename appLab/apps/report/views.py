import plotly.graph_objs as go
import plotly.io as pio
from typing import Any
from django.views.generic import TemplateView, FormView
from .forms import ResultsClassSelect
from apps.attendance.models import Students, TecnoEnabledResults

# Create your views here.
class EnabledTecnologicResultsView(FormView):
    template_name = 'report/resultsTecnologic.html'
    form_class = ResultsClassSelect

class GlobalEnabledView(TemplateView):
    template_name = 'report/globalEnabledStudents.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(GlobalEnabledView, self).get_context_data(**kwargs)
        
        total_students = Students.objects.count()
        no_habilitados = TecnoEnabledResults.objects.filter(status=False).values('student').distinct().count()
        habilitados = total_students - no_habilitados

        print(total_students, habilitados, no_habilitados)
        
        # Datos para el gráfico de torta
        labels = ['Habilitados', 'No habilitados']
        values = [habilitados, no_habilitados]

        # Crear el gráfico de torta con Plotly
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])


        context['total_students'] = total_students
        context['enabled_students'] = habilitados
        context['disabled_students'] = no_habilitados
        context['plot_div'] = pio.to_html(fig, full_html=False)

        return context