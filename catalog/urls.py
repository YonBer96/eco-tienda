from django.urls import path

from .views import product_table

urlpatterns = [
    path('', product_table, name='product_table'),
]
