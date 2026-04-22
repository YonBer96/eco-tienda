from decimal import Decimal

from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    contacto = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class CategoriaProducto(models.Model):
    FRUTAS = 'Frutas'
    HORTALIZAS = 'Hortalizas'
    ENVASADOS = 'Envasados'
    FRUTOS_SECOS = 'Frutos secos'
    BEBIDAS = 'Bebidas'

    NOMBRES_PREDETERMINADOS = [
        FRUTAS,
        HORTALIZAS,
        ENVASADOS,
        FRUTOS_SECOS,
        BEBIDAS,
    ]

    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categorías de producto'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @classmethod
    def ordered_queryset(cls):
        preferred_order = models.Case(
            models.When(nombre=cls.FRUTAS, then=models.Value(0)),
            models.When(nombre=cls.HORTALIZAS, then=models.Value(1)),
            models.When(nombre=cls.ENVASADOS, then=models.Value(2)),
            models.When(nombre=cls.FRUTOS_SECOS, then=models.Value(3)),
            models.When(nombre=cls.BEBIDAS, then=models.Value(4)),
            default=models.Value(99),
            output_field=models.IntegerField(),
        )
        return cls.objects.annotate(_preferred_order=preferred_order).order_by('_preferred_order', 'nombre')


class Producto(models.Model):
    KG = 'kg'
    UNIDAD = 'ud'
    DOCENA = 'docena'
    LITRO = 'l'
    MANOJO = 'manojo'
    CAJA = 'caja'
    BANDEJA = 'bandeja'
    BOTE = 'bote'
    GARRAFA = 'garrafa'

    UNIDADES_MEDIDA = [
        (KG, 'Kilogramo'),
        (UNIDAD, 'Unidad'),
        (DOCENA, 'Docena'),
        (LITRO, 'Litro'),
        (MANOJO, 'Manojo'),
        (CAJA, 'Caja'),
        (BANDEJA, 'Bandeja'),
        (BOTE, 'Bote'),
        (GARRAFA, 'Garrafa'),
    ]

    IVA_4 = Decimal('4.00')
    IVA_10 = Decimal('10.00')
    IVA_CHOICES = [
        (IVA_4, '4%'),
        (IVA_10, '10%'),
    ]

    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='productos')
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    iva = models.DecimalField(max_digits=4, decimal_places=2, choices=IVA_CHOICES, default=IVA_4)
    unidad_medida = models.CharField(max_length=20, choices=UNIDADES_MEDIDA, default=KG)
    pedido_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    incremento_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.50'))
    stock_disponible = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    limitar_stock = models.BooleanField(default=False)
    formato_caja = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Cantidad por caja para pedir al proveedor. Ejemplo: 5 kg o 5 ud por caja.')
    origen = models.CharField(max_length=150, blank=True, help_text='Origen o procedencia del producto. Ejemplo: Huelva, Valencia, cooperativa local, etc.')
    descripcion = models.CharField(max_length=255, blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
