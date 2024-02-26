from django import forms

class StudentFoundForm(forms.Form):
    rut = forms.CharField(
        label="RUT",
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            "id": "rut",
            "placeholder": "Ingresa un RUT sin puntos ni guión.",
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
            "class": "outline outline-1 outline-gray-300 text-center text-xl",
        }),
    )




  