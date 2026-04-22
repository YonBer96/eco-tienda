from django.urls import path

from . import views

urlpatterns = [
    path('', views.pedido_list, name='pedido_list'),
    path('nuevo/', views.pedido_create, name='pedido_create'),
    path('<int:pk>/', views.pedido_detail, name='pedido_detail'),
    path('<int:pk>/editar/', views.pedido_edit, name='pedido_edit'),
    path('<int:pk>/eliminar/', views.pedido_delete, name='pedido_delete'),
]
