from django.urls import path
from .views import AttendanceFormView, StudentFoundFormView, StudentsCreateView

app_name = 'attendance_app'

urlpatterns = [
    path('', StudentFoundFormView.as_view(), name="student"),
    path('asistencia/<str:student>/', AttendanceFormView.as_view(), name="attendance"),
    path('estudiante/add/',StudentsCreateView.as_view(), name="student-add"),
]