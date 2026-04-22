from django import forms
from django.contrib.auth.models import User

from .models import PerfilUsuario


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['telefono', 'direccion']
        widgets = {'direccion': forms.Textarea(attrs={'rows': 3})}
