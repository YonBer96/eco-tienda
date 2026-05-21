from django import forms

from .models import OrderCycle
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



class OrderCycleForm(forms.ModelForm):
    DIAS = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    dias_reparto = forms.MultipleChoiceField(
        choices=DIAS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Días de reparto'
    )

    class Meta:
        model = OrderCycle
        fields = [
            'nombre',
            'inicio',
            'cierre',
            'dias_reparto',
            'cerrado',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'inicio': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
            'cierre': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
            'cerrado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.dias_reparto:
            self.initial['dias_reparto'] = [d.strip() for d in self.instance.dias_reparto.split(',') if d.strip()]

    def clean_dias_reparto(self):
        dias = self.cleaned_data.get('dias_reparto') or []
        return ','.join(dias)
