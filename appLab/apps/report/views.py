from django.views.generic import TemplateView, FormView
from .forms import ResultsClassSelect

# Create your views here.
class EnabledTecnologicResultsView(FormView):
    template_name = 'report/resultsTecnologic.html'
    form_class = ResultsClassSelect