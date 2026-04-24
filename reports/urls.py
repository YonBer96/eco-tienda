from django.urls import path
from . import views

urlpatterns = [
    path('pedido/<int:pedido_id>/pdf/', views.albaran_individual_pdf, name='albaran_individual_pdf'),
    path('pedido/<int:pedido_id>/factura/', views.factura_pdf, name='factura_pdf'),
    path('pedido/<int:pedido_id>/email/', views.enviar_albaran_email, name='enviar_albaran_email'),
    path('proveedor/<int:proveedor_id>/email/', views.supplier_email_draft, name='supplier_email_draft'),
    path('semanal/', views.weekly_summary, name='weekly_summary'),
    path('semanal/pdf/', views.weekly_summary_pdf, name='weekly_summary_pdf'),
    path('proveedores/', views.supplier_summary, name='supplier_summary'),
    path('proveedores/pdf/', views.supplier_summary_pdf, name='supplier_summary_pdf'),
    path('ciclo/<int:ciclo_id>/general/pdf/', views.albaran_semanal_general_pdf, name='albaran_semanal_general_pdf'),
    path('ciclo/<int:ciclo_id>/proveedores/pdf/', views.albaran_por_proveedor_pdf, name='albaran_por_proveedor_pdf'),
]
