from django import forms
from .models import Classes
from django.contrib import messages

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


class ExelFormStudents(forms.Form):

    file = forms.FileField(
        label="Selecciona un archivo",
    )

    class_name = forms.ModelChoiceField(
        label='Asignatura',
        queryset=Classes.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                "id": "class_name",
                "class": "py-2 outline outline-1 outline-gray-300 xl:text-xl",
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        class_name = cleaned_data.get("class_name")

        if class_name is not None and class_name not in self.fields['class_name'].queryset:
            raise forms.ValidationError("La asignatura seleccionada no es válida.")
        
        return cleaned_data

    
        
    
    

   