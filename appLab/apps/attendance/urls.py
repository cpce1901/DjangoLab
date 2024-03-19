from django.urls import path
from .views import AttendanceFormView, StudentFoundFormView, TeamsView, TeamsFilterView

app_name = 'attendance_app'

urlpatterns = [
    path('', StudentFoundFormView.as_view(), name="student"),
    path('asistencia/<str:student>/', AttendanceFormView.as_view(), name="attendance"),
    path('grupos/', TeamsView.as_view(), name='teams'),
]

htmx_urlpatterns = [
    path('grupos/filtro/', TeamsFilterView, name='teams-filter')
]

urlpatterns += htmx_urlpatterns
