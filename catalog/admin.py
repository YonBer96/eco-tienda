from django.contrib import admin

from .models import CategoriaProducto, Producto, Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'telefono', 'email', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'contacto', 'email', 'telefono')


@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'categoria', 'proveedor', 'origen', 'precio', 'iva', 'unidad_medida',
        'pedido_minimo', 'incremento_pedido', 'formato_caja', 'activo'
    )
    list_filter = ('activo', 'categoria', 'proveedor', 'unidad_medida', 'iva')
    search_fields = ('nombre', 'descripcion', 'origen')
    list_editable = (
        'categoria', 'proveedor', 'origen', 'precio', 'iva', 'unidad_medida',
        'pedido_minimo', 'incremento_pedido', 'formato_caja', 'activo'
    )
