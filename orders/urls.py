from django.urls import path
from .views import cycle_list, cycle_create, cycle_update, cycle_delete
from . import views

urlpatterns = [
    path('', views.pedido_list, name='pedido_list'),
    path('nuevo/', views.pedido_create, name='pedido_create'),
    path('<int:pk>/', views.pedido_detail, name='pedido_detail'),
    path('<int:pk>/editar/', views.pedido_edit, name='pedido_edit'),
    path('<int:pk>/eliminar/', views.pedido_delete, name='pedido_delete'),
    path('ciclos/', cycle_list, name='cycle_list'),
    path('ciclos/nuevo/', cycle_create, name='cycle_create'),
    path('ciclos/<int:pk>/editar/', cycle_update, name='cycle_update'),
    path('ciclos/<int:pk>/cerrar/', cycle_delete, name='cycle_delete'),
]
