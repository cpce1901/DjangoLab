from django.views.generic import FormView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import Students, Attendance
from .form import AttendanceForm, StudentFoundForm, StudentCreateForm
from datetime import datetime, timedelta


# Create your views here.
class StudentFoundFormView(FormView):
    template_name = 'attendance/studentFoundForm.html'
    form_class = StudentFoundForm
    success_url = reverse_lazy("attendance_app:attendance")

    def form_valid(self, form):
        rut = form.cleaned_data["rut"]
        student = Students.objects.filter(rut = rut).first()              
 
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
                "El RUT no coincide con ningún estudiante. Inténtalo otra vez."
            )
            return self.form_invalid(form)
            

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
        

class StudentsCreateView(FormView):
    template_name = 'attendance/studentAdd.html'
    form_class = StudentCreateForm
    success_url = reverse_lazy("attendance_app:student-add")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        last_name = form.cleaned_data["last_name"]
        rut = form.cleaned_data["rut"]
        email = form.cleaned_data["email"]

        try:
            new_student = Students(name=name, last_name=last_name, rut=rut, email=email)
            new_student.save()

            messages.success(
            self.request,
            f"Alumno: {name} ingresado con exito."
            )

            return redirect(reverse_lazy("attendance_app:student-add"))

        except:

            messages.error(
            self.request,
            f"No se ha podiso realizar el ingreso."
            )

            return self.form_invalid(form)

        
