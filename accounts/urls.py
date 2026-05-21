from django.urls import path

from .views import (
    CustomPasswordChangeView,
<<<<<<< HEAD
    cliente_create,
    cliente_delete,
    cliente_list,
    cliente_update,
    profile_edit,
    tienda_create,
    tienda_delete,
    tienda_list,
    tienda_update,
=======
    profile_edit,
    cliente_list,
    cliente_create,
    cliente_update,
    cliente_delete,
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e
)

urlpatterns = [
    path('perfil/', profile_edit, name='profile_edit'),
    path('password/', CustomPasswordChangeView.as_view(), name='password_change'),

    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', cliente_delete, name='cliente_delete'),
<<<<<<< HEAD

    path('tiendas/', tienda_list, name='tienda_list'),
    path('tiendas/nueva/', tienda_create, name='tienda_create'),
    path('tiendas/<int:pk>/editar/', tienda_update, name='tienda_update'),
    path('tiendas/<int:pk>/eliminar/', tienda_delete, name='tienda_delete'),
]
=======
]
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e
