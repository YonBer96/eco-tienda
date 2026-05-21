from django import forms
from django.contrib.auth.models import User

from .models import Cliente, PerfilUsuario, Tienda


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['telefono', 'direccion']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'nif',
            'telefono',
            'email',
            'direccion',
            'direccion_facturacion',
            'activo',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nif': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'direccion_facturacion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ClienteCreateForm(ClienteForm):
    username = forms.CharField(
        label='Usuario de acceso',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Repetir contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Ya existe un usuario con ese nombre.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned_data


class TiendaForm(forms.ModelForm):
    class Meta:
        model = Tienda
        fields = [
            'cliente',
            'nombre',
            'direccion',
            'direccion_facturacion',
            'telefono',
            'email',
            'activa',
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'direccion_facturacion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
