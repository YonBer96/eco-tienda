from django import forms

from .models import Proveedor
from .models import Producto

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'nombre',
            'contacto',
            'telefono',
            'email',
            'direccion',
            'observaciones',
            'activo',
        ]
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'categoria',
            'proveedor',
            'origen',
            'precio',
            'iva',
            'unidad_medida',
            'pedido_minimo',
            
            'activo',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'origen': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pedido_minimo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'paso_pedido': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }