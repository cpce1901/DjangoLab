from django import forms
from apps.attendance.models import Classes

class ResultsClassSelect(forms.Form):
    class_name = forms.ModelChoiceField(
        label='Asignatura',
        queryset=Classes.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                "hx-get": "filtro/",
                "hx-trigger": "change",
                "hx-target": "#response",
                "class": "p-2 outline outline-1 outline-gray-300 bg-white rounded-lg",
            }
        )
    )