from django import forms
from django.contrib.auth.models import User
<<<<<<< HEAD

from .models import Cliente, PerfilUsuario, Tienda
=======
from .models import Cliente, Tienda
from .models import PerfilUsuario

>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
<<<<<<< HEAD
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
=======
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['telefono', 'direccion']
<<<<<<< HEAD
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
=======
        widgets = {'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
                   'direccion_facturacion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
}
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e


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
<<<<<<< HEAD
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


=======
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'direccion_facturacion': forms.Textarea(attrs={'rows': 3}),
        }


>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e
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
<<<<<<< HEAD
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'direccion_facturacion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
=======
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'direccion_facturacion': forms.Textarea(attrs={'rows': 3}),
        }
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e
