from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .models import CategoriaProducto, Producto


@login_required
def product_table(request):
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '').strip()
    productos = Producto.objects.filter(activo=True).select_related('categoria', 'proveedor').order_by('nombre')

    if query:
        productos = productos.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query) | Q(origen__icontains=query))
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    categorias = CategoriaProducto.ordered_queryset()
    return render(request, 'catalog/product_table.html', {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_id': categoria_id,
    })
