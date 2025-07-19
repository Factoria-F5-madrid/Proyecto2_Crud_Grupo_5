from django import forms
from .models import Usuaria

class DatosUsuariaForm(forms.ModelForm):
    class Meta:
        model = Usuaria
        fields = ['nombre', 'email', 'telefono', 'direccion']

