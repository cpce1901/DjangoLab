from django.urls import path
from .views import AttendanceFormView, StudentFoundFormView

app_name = 'attendance_app'

urlpatterns = [
    path('estudiante/', StudentFoundFormView.as_view(), name="student"),
    path('asistencia/<str:student>/', AttendanceFormView.as_view(), name="attendance"),
]