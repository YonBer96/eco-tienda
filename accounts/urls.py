from django.urls import path

from .views import (
    CustomPasswordChangeView,
    profile_edit,
    cliente_list,
    cliente_create,
    cliente_update,
    cliente_delete,
)

urlpatterns = [
    path('perfil/', profile_edit, name='profile_edit'),
    path('password/', CustomPasswordChangeView.as_view(), name='password_change'),

    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', cliente_delete, name='cliente_delete'),
]