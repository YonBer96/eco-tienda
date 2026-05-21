from django.urls import path

from .views import (
    CustomPasswordChangeView,
    cliente_create,
    cliente_delete,
    cliente_list,
    cliente_update,
    profile_edit,
    tienda_create,
    tienda_delete,
    tienda_list,
    tienda_update,
)

urlpatterns = [
    path('perfil/', profile_edit, name='profile_edit'),
    path('password/', CustomPasswordChangeView.as_view(), name='password_change'),

    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', cliente_delete, name='cliente_delete'),

    path('tiendas/', tienda_list, name='tienda_list'),
    path('tiendas/nueva/', tienda_create, name='tienda_create'),
    path('tiendas/<int:pk>/editar/', tienda_update, name='tienda_update'),
    path('tiendas/<int:pk>/eliminar/', tienda_delete, name='tienda_delete'),
]
