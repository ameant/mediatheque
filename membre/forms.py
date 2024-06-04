from django import forms
from .models import Emprunteur

class EmprunteurUpdateForm(forms.ModelForm):
    class Meta:
        model = Emprunteur
        fields = ['name', 'blocked']
        labels = {
            'name': 'Nom',
            'blocked': 'Bloquer le membre'
        }