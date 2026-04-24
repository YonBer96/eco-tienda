from django import forms

from accounts.models import Cliente, Tienda
from .models import Pedido


class PedidoMetaForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'tienda', 'observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'rows': 2})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['tienda'].required = True
        if user and not user.is_superuser:
            clientes = Cliente.objects.filter(usuarios=user, activo=True).distinct()
            self.fields['cliente'].queryset = clientes
            self.fields['tienda'].queryset = Tienda.objects.filter(cliente__in=clientes, activa=True).distinct()
        else:
            self.fields['cliente'].queryset = Cliente.objects.filter(activo=True)
            self.fields['tienda'].queryset = Tienda.objects.filter(activa=True)
