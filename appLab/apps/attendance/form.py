from django import forms
from .models import TopicEnabled

class StudentFoundForm(forms.Form):
    email = forms.CharField(
        label="USUARIO",
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            "id": "email",
            "placeholder": "Ingresa tu usuario",
            "class": "text-input",
        }),
    )


class AttendanceForm(forms.Form): 

    OPTIONS = (
        (0, '--'),
        (1, '1 hr'),
        (2, '2 hrs'),
        (3, '3 hrs'),
    )

    time_inside = forms.IntegerField(
        label="Estadia aproximada",
        required=True,
        widget=forms.Select(
            choices=OPTIONS,
            attrs={
            "id": "time_inside",
            "class": "py-2 outline outline-1 outline-gray-300 text-center xl:text-xl",
        }),
    )


class ExelForm(forms.Form):
        
    file = forms.FileField(
        label="Selecciona un archivo",
    )

    

   