
import pandas as pd
from django.shortcuts import render
from django.views.generic import FormView,TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import Students, Attendance, Teams, TopicEnabled, TecnoEnabledResults
from .form import AttendanceForm, StudentFoundForm, ExelForm
from datetime import datetime, timedelta


# Vista Inicial Ingreso a Lab
class StudentFoundFormView(FormView):
    template_name = 'attendance/studentFoundForm.html'
    form_class = StudentFoundForm
    success_url = reverse_lazy("attendance_app:attendance")

    def form_valid(self, form):
        user = form.cleaned_data["email"]
        email = user + '@correo.uss.cl'
        student = Students.objects.filter(email=email).first()              
 
        if student:
            id_student = student.id
            latest_attendance = Attendance.objects.filter(student_id=student.id).order_by('-date_in', '-time_inside').first()

            if latest_attendance:
                when_in_time = latest_attendance.date_in
                time_inside_time = latest_attendance.time_inside
                time_now = datetime.now()               

                # Convert when_in_time.time() to datetime.timedelta
                when_in_time_timedelta = timedelta(hours=when_in_time.hour, minutes=when_in_time.minute, seconds=when_in_time.second)
                time_inside_time_timedelta = timedelta(hours=time_inside_time.hour, minutes=time_inside_time.minute, seconds=time_inside_time.second)
                time_now_delta = timedelta(hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second)

                # Tiempo y Fecha de entrada + tiempo solicitado
                time_start_inside = when_in_time + time_inside_time_timedelta

                # Tiempo de entrada + tiempo solicitado
                total_time = when_in_time_timedelta + time_inside_time_timedelta
                            
                if time_now > time_start_inside:
                    return redirect(reverse_lazy("attendance_app:attendance", kwargs={'student': id_student}))
                else:            
                    remaining_time = total_time - time_now_delta
                    messages.info(
                    self.request,
                    f"Tienes un registro de ingreso a las {when_in_time.strftime('%H:%M:%S')} por {time_inside_time.hour} hr(s), aún tienes tiempo en el laboratorio. Falta {remaining_time}. "
                    )
                    return self.form_invalid(form)
            else:
                return redirect(reverse_lazy("attendance_app:attendance", kwargs={'student': id_student}))
        else:            
            messages.error(
                self.request,
                "El usuario no coincide con ningún estudiante. Recuerda que tu usuario es la primera parte de tu correo"
            )
            return self.form_invalid(form)
      
            
# Vista tiempo Ingreso a Lab
class AttendanceFormView(FormView):
    template_name = 'attendance/attendanceForm.html'
    form_class = AttendanceForm
    success_url = "/thanks/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student']

        student = Students.objects.filter(id = student_id).first()

        context["student"] = student
        
        return context

    def form_valid(self, form):
        student_id = self.kwargs['student']
        time_inside = form.cleaned_data["time_inside"]

        if time_inside <= 0 or time_inside > 3:
            messages.error(
                self.request,
                "Debes seleccionar un tiempo valido de estadia..."
            )
            return self.form_invalid(form)
        
        if time_inside > 0:

            time_inside = str(timedelta(hours=time_inside))
           
            student = Students.objects.filter(id = student_id).first()

            attendance = Attendance.objects.create(student=student, time_inside=time_inside) 
            attendance.save()

            return redirect(reverse_lazy("attendance_app:attendance", kwargs={'student': student_id}) + "?ok")


# Vista para mostrar grupos
class TeamsView(TemplateView):
    template_name = 'attendance/admin/teamsList.html'

    
    def get_context_data(self, **kwargs):
        context = super(TeamsView, self).get_context_data(**kwargs)
        context['teams'] = Teams.objects.all()
        return context
    

# Vista para mostrar grupos
class StudentsView(TemplateView):
    template_name = 'attendance/admin/studentDetail.html'

    

class ExelUploadForm(FormView):
    template_name = 'attendance/admin/uploadExel.html'
    form_class = ExelForm
    success_url = reverse_lazy("attendance_app:student")
    

    def form_valid(self, form):
        uploaded_file = self.request.FILES['file']
        
        extention = uploaded_file.name.split('.')[-1].lower()
        if extention != 'xlsx':
            messages.error(
                self.request,
                "El formato de archivo es invalido, debes subir un archivo .xlsx"
            )
            return self.form_invalid(form)

        df = pd.read_excel(uploaded_file, header=1, usecols=['Nombre', 'Apellidos', 'Tareas', 'Puntos', 'Puntos máximos'])
        df['Puntos'] = df['Puntos'].fillna(0).astype(int)

        # tester-dev: ICMI:OK
        for i in range (int(len(df))):
            student = Students.objects.filter(last_name__icontains=df["Apellidos"][i]).first()
            if student is not None:
                if 'internet de las cosas'.lower() in str(df['Tareas'][i]).lower():
                    topic_id=1
                elif '3D'.lower() in str(df['Tareas'][i]).lower():
                    topic_id=2
                elif 'cobot'.lower() in str(df['Tareas'][i]).lower():
                    topic_id=3
                elif 'gladius'.lower() in str(df['Tareas'][i]).lower():
                    topic_id=4
                elif 'dron dji'.lower() in str(df['Tareas'][i]).lower():
                    topic_id=5
                elif 'realidad virtual'.lower() in str(df['Tareas'][i]).lower():
                    topic_id=6
                elif 'jetauto'.lower() in str(df['Tareas'][i]).lower():
                    topic_id=7
                elif 'ia'.lower() in str(df['Tareas'][i]).lower():
                    topic_id=8
                else:
                    break

                TecnoEnabledResults.objects.update_or_create(
                    student=student,
                    topic_id=topic_id,
                    defaults={
                        'score_result': df['Puntos'][i],
                        'status': df['Puntos'][i] is not None and df['Puntos'][i] >= 60
                    }
                )

        messages.success(
            self.request,
            "Archivo subido con exito"
        )
        return redirect(reverse_lazy("attendance_app:update-data"))