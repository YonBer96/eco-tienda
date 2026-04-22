from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.db import models
from django.utils import timezone

from accounts.models import Cliente, Tienda
from catalog.models import Producto, Proveedor
from core.utils import ordering_window_open


def quantize_2(value):
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class OrderCycle(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    inicio = models.DateTimeField()
    cierre = models.DateTimeField()
    reparto_inicio = models.DateTimeField(null=True, blank=True)
    reparto_fin = models.DateTimeField(null=True, blank=True)
    cerrado = models.BooleanField(default=False)

    class Meta:
        ordering = ['-inicio']

    def __str__(self):
        return self.nombre

    @property
    def esta_abierto(self):
        now = timezone.now()
        return self.inicio <= now <= self.cierre and not self.cerrado


class Pedido(models.Model):
    BORRADOR = 'borrador'
    CONFIRMADO = 'confirmado'
    ANULADO = 'anulado'
    ESTADOS = [
        (BORRADOR, 'Borrador'),
        (CONFIRMADO, 'Confirmado'),
        (ANULADO, 'Anulado'),
    ]

    ciclo = models.ForeignKey(OrderCycle, on_delete=models.PROTECT, related_name='pedidos')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='pedidos')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    tienda = models.ForeignKey(Tienda, on_delete=models.PROTECT, related_name='pedidos')
    estado = models.CharField(max_length=20, choices=ESTADOS, default=BORRADOR)
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado_en']
        constraints = [
            models.UniqueConstraint(fields=['ciclo', 'tienda'], name='unique_pedido_tienda_ciclo')
        ]

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente.nombre}'

    @property
    def subtotal(self):
        return quantize_2(sum((linea.subtotal for linea in self.lineas.all()), Decimal('0.00')))

    @property
    def total_iva(self):
        return quantize_2(sum((linea.iva_total for linea in self.lineas.all()), Decimal('0.00')))

    @property
    def total(self):
        return quantize_2(self.subtotal + self.total_iva)

    def puede_editarse_por(self, user):
        if user.is_superuser:
            return True
        if self.usuario_id != user.id:
            return False
        if self.estado == self.ANULADO:
            return False
        return self.ciclo.esta_abierto and ordering_window_open()


class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    proveedor_snapshot = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='+')
    nombre_producto_snapshot = models.CharField(max_length=150)
    unidad_medida_snapshot = models.CharField(max_length=20)
    precio_unitario_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    iva_snapshot = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('4.00'))
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        ordering = ['nombre_producto_snapshot']
        unique_together = ('pedido', 'producto')

    def __str__(self):
        return f'{self.nombre_producto_snapshot} ({self.cantidad})'

    def save(self, *args, **kwargs):
        self.cantidad = quantize_2(self.cantidad)
        self.precio_unitario_snapshot = quantize_2(self.precio_unitario_snapshot)
        self.iva_snapshot = quantize_2(self.iva_snapshot)
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return quantize_2(self.cantidad * self.precio_unitario_snapshot)

    @property
    def iva_total(self):
        return quantize_2(self.subtotal * (self.iva_snapshot / Decimal('100')))

    @property
    def total_con_iva(self):
        return quantize_2(self.subtotal + self.iva_total)
