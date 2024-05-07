from datetime import datetime
from django import forms
from .models import Gives, Materials, Items

class GivesAdminForm(forms.ModelForm):
    class Meta:
        model = Gives
        fields = ['student', 'date_back', 'observations']
        

    def clean(self):
        cleaned_data = super().clean()

        student = cleaned_data.get('student')
        date_out = datetime.now().date()
        date_back = datetime.strptime(str(cleaned_data.get('date_back')), "%Y-%m-%d").date()
        instance = self.instance

        if date_back < date_out:
            self.add_error(
                'date_back',
                f"La fecha de devolución {date_back}, no puede ser menor a la fecha de hoy."
            )

        
        if student and instance:
            existing_gives = Gives.objects.filter(student=student).exclude(id=instance.id)
            if existing_gives.exists():
                self.add_error(
                    'student',
                    f"El estudiante {student.name} ya tiene un préstamo activo."
                )

        return cleaned_data
    

class ItemsForm(forms.ModelForm):

    class Meta:
        model = Items
        fields = ['gives', 'item', 'count_save', 'count', 'is_back']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['count_save'].widget.attrs['readonly'] = True
        

    def clean(self):
        cleaned_data = super().clean()
        count = cleaned_data.get('count')
        item = cleaned_data.get('item')
        is_back = cleaned_data.get('is_back')

        if not isinstance(count, int):
            self.add_error(
                'count',
                "El valor ingresado no es un número entero"
            )

        if item is not None and count is not None and count > item.stock and not is_back:
            self.add_error(
                'count',
                f"La cantidad solicitada ({count}) excede el stock disponible ({item.stock}) para el material '{item.description}'."
            )

        return cleaned_data


