from django.urls import path

from .views import (
    product_table,
    proveedor_list,
    proveedor_create,
    proveedor_update,
    proveedor_delete,
)
from .views import producto_list, producto_create, producto_update, producto_delete,producto_update_inline

urlpatterns = [
    path('', product_table, name='product_table'),

    path('proveedores/', proveedor_list, name='proveedor_list'),
    path('proveedores/nuevo/', proveedor_create, name='proveedor_create'),
    path('proveedores/<int:pk>/editar/', proveedor_update, name='proveedor_update'),
    path('proveedores/<int:pk>/eliminar/', proveedor_delete, name='proveedor_delete'),
    path('productos/', producto_list, name='producto_list'),
    path('productos/nuevo/', producto_create, name='producto_create'),
    path('productos/<int:pk>/editar/', producto_update, name='producto_update'),
    path('productos/<int:pk>/eliminar/', producto_delete, name='producto_delete'),
    path('productos/<int:pk>/inline/', producto_update_inline, name='producto_update_inline'),
]