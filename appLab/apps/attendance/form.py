from django import forms
from .models import Students

class StudentFoundForm(forms.Form):
    email = forms.CharField(
        label="USUARIO",
        max_length=10,
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


class StudentCreateForm(forms.Form):
    
    name = forms.CharField(
        label="Nombre",
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            "id": "name",
            "placeholder": "Ingresa tu nombre",
            "class": "text-input",
        }),
    )

    last_name = forms.CharField(
        label="Apellido",
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            "id": "last_name",
            "placeholder": "Ingresa tu apellido",
            "class": "text-input",
        }),
    )

    rut = forms.CharField(
        label="RUT",
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            "id": "rut",
            "placeholder": "RUT sin puntos ni guión.",
            "class": "text-input",
        }),
    )

    email = forms.EmailField(
        label="e-mail",
        required=True,
        widget=forms.EmailInput(attrs={
            "id": "email",
            "placeholder": "Ingresa tu correo.",
            "class": "text-input",
        }),
    )




  