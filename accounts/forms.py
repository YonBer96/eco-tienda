from django import forms
from django.contrib.auth.models import User
from .models import Cliente, Tienda
from .models import PerfilUsuario



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['telefono', 'direccion']
        widgets = {'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
                   'direccion_facturacion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'direccion_facturacion': forms.Textarea(attrs={'rows': 3}),
        }


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
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'direccion_facturacion': forms.Textarea(attrs={'rows': 3}),
        }