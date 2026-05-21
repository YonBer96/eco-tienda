from django.conf import settings
from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    nif = models.CharField(max_length=20, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    direccion_facturacion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='clientes', blank=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Tienda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='tiendas')
    nombre = models.CharField(max_length=150)
    direccion = models.TextField(blank=True)
    direccion_facturacion = models.TextField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['cliente__nombre', 'nombre']
        unique_together = ('cliente', 'nombre')

    def __str__(self):
        return f'{self.nombre} - {self.cliente.nombre}'


class PerfilUsuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_username()
