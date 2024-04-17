
import pandas as pd
from django.shortcuts import render
from django.views.generic import FormView,TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import Students, Attendance, Teams, TopicEnabled, TecnoEnabledResults
from .form import AttendanceForm, StudentFoundForm, ExelForm, ExelFormStudents, Classes
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
    
    def change_name_by_id(self, task):

        if 'artificial' in task:
            return TopicEnabled.objects.filter(name='IA').first().id
        elif 'jetauto' in task:
            return TopicEnabled.objects.filter(name='ROV').first().id
        elif 'aumentada' in task:
            return TopicEnabled.objects.filter(name='VR').first().id
        elif 'dron' in task:
            return TopicEnabled.objects.filter(name='DRON').first().id
        elif 'gladius' in task:
            return TopicEnabled.objects.filter(name='GLADIUS').first().id
        elif 'cobot' in task:
            return TopicEnabled.objects.filter(name='COBOT').first().id
        elif 'fabricación' in task:
            return TopicEnabled.objects.filter(name='F3D').first().id
        elif 'internet de las cosas' in task:
            return TopicEnabled.objects.filter(name='IOT').first().id
        
    def form_valid(self, form):
        uploaded_file = self.request.FILES['file']
        
        extention = uploaded_file.name.split('.')[-1].lower()
        if extention != 'xlsx':
            messages.error(
                self.request,
                "El formato de archivo es invalido, debes subir un archivo .xlsx"
            )
            return self.form_invalid(form)

        df = pd.read_excel(uploaded_file, header=1, usecols=['Nombre', 'Apellidos', 'Dirección de correo electrónico', 'Tareas', 'Puntos', 'Puntos máximos'])
        df['Puntos'] = df['Puntos'].fillna(0).astype(int)

        for i in range(int(len(df))):   
            try:       
                student = Students.objects.get(email=df["Dirección de correo electrónico"][i])
                task = str(df['Tareas'][i]).lower().strip()

                topic_id = self.change_name_by_id(task)

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
            
            except:
                messages.error(
                self.request,
                "El formato de archivo es invalido, debes subir un archivo .xlsx"
                )
                
            return self.form_invalid(form)
                   
        
    


class ExelUploadStudents(FormView):
    template_name = 'attendance/admin/uploadExelStudents.html'
    form_class = ExelFormStudents
    success_url = reverse_lazy("attendance_app:student")
    
          
    def form_valid(self, form):
        uploaded_file = self.request.FILES['file']
        class_name = form.cleaned_data["class_name"]
        users_to_update = []
        users_to_create = []

        print(class_name)

        # Leer extension de archivo exel
        extention = uploaded_file.name.split('.')[-1].lower()
        if extention != 'xlsx':
            messages.error(
                self.request,
                "El formato de archivo es invalido, debes subir un archivo .xlsx"
            )
            return self.form_invalid(form)

        # Leer archivo exel para conseguir header y nombre de ASIGNATURA
        df_one = pd.read_excel(uploaded_file)
        
        if not df_one.columns.str.contains(str(class_name.school.code)).any():
            messages.error(
                self.request,
                "El archivo subido no corresponde a la asignatura"
            )
            return self.form_invalid(form)

        # Leer archivo exel con los header de la segunda linea
        df = pd.read_excel(uploaded_file, header=1, usecols=['Nombre', 'Apellidos', 'Dirección de correo electrónico'])
        
        for index, row in df.iterrows():
            student = Students.objects.filter(email=row['Dirección de correo electrónico']).first()
            if student is None:
                # Agregar al listado de estudiantes a crear
                users_to_create.append(Students(name=row['Nombre'], last_name=row['Apellidos'], email=row['Dirección de correo electrónico'], class_name=class_name))
            else:
                # Agregar al listado de estudiantes a actualizar
                student.name = row['Nombre']
                student.last_name = row['Apellidos']
                student.email = row['Dirección de correo electrónico']
                student.class_name = class_name
                users_to_update.append(student)

        if users_to_create:
            try:
                Students.objects.bulk_create(users_to_create)
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    messages.error(
                    self.request,
                    "El archivo contiene usuarios duplicados. Por favor, revisa el archivo y elimina las entradas duplicadas."
                )
                else:
                    messages.error(
                    self.request,
                    "Puede que tu archivo no sea correcto. Por favor, revísalo e inténtalo nuevamente."
                )
                
                return self.form_invalid(form)

        if users_to_update:
            try:
                Students.objects.bulk_update(users_to_update, ['name', 'last_name', 'email', 'class_name'])
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    messages.error(
                    self.request,
                    "El archivo contiene usuarios duplicados. Por favor, revisa el archivo y elimina las entradas duplicadas."
                )
                else:
                    messages.error(
                    self.request,
                    "Puede que tu archivo no sea correcto. Por favor, revísalo e inténtalo nuevamente."
                )
                
                return self.form_invalid(form)
              
        messages.success(
        self.request,
        "Archivo subido con exito"
        )
        return redirect(reverse_lazy("attendance_app:update-data-students"))