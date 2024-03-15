from django.urls import path
from .views import AttendanceFormView, StudentFoundFormView, StudentsCreateView, SchoolListView, ClassesListView, TeamsListView

app_name = 'attendance_app'

urlpatterns = [
    path('', StudentFoundFormView.as_view(), name="student"),
    path('asistencia/<str:student>/', AttendanceFormView.as_view(), name="attendance"),
    path('escuela/', SchoolListView.as_view(), name="schools"),
    path('escuela/clase/<int:school>/', ClassesListView.as_view(), name="class"),
    path('escuela/clase/teams/<int:team>/', TeamsListView.as_view(), name="teams"),
    path('estudiante/<int:team>/add/',StudentsCreateView.as_view(), name="student-add"),
]