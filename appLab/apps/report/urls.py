from django.urls import path
from .views import EnabledTecnologicResultsView
from .views_htmx import ResultsFilterView

app_name = 'report_app'

urlpatterns = [
    path('results/', EnabledTecnologicResultsView.as_view(), name="report"),
]

htmx_urlpatterns = [
    path('results/filtro/', ResultsFilterView, name="report-filter"),
]

urlpatterns += htmx_urlpatterns