from django import forms
from .models import GivesTotal

class GivesForm(forms.ModelForm):

    class Meta:
        model = GivesTotal
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super().clean()
        is_back = cleaned_data.get('is_back')
    
            
        return cleaned_data

    