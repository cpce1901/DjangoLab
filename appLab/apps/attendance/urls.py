from django.urls import path
from .views import AttendanceFormView, StudentFoundFormView, TeamsView, StudentsView, ExelUploadForm, ExelUploadStudents
from .views_htmx import TeamsFilterView, StudentFilterView

app_name = 'attendance_app'

urlpatterns = [
    path('', StudentFoundFormView.as_view(), name="student"),
    path('asistencia/<str:student>/', AttendanceFormView.as_view(), name="attendance"),
    path('grupos/', TeamsView.as_view(), name='teams'),
    path('estudiantes/', StudentsView.as_view(), name='students'),
    path('exel/update/', ExelUploadForm.as_view(), name='update-data'),
    path('exel/update/estudiantes/', ExelUploadStudents.as_view(), name='update-data-students'),
]

htmx_urlpatterns = [
    path('grupos/filtro/', TeamsFilterView, name='teams-filter'),
    path('estudiantes/filtro/',StudentFilterView , name='students-filter')
]

urlpatterns += htmx_urlpatterns
