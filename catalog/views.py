from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .models import CategoriaProducto, Producto
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .forms import ProveedorForm
from .models import CategoriaProducto, Producto, Proveedor
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Producto
from .forms import ProductoForm


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

def admin_required(user):
    return user.is_superuser


@login_required
@user_passes_test(admin_required)
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'catalog/proveedor_list.html', {'proveedores': proveedores})


@login_required
@user_passes_test(admin_required)
def proveedor_create(request):
    form = ProveedorForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Proveedor creado correctamente.')
        return redirect('proveedor_list')
    return render(request, 'catalog/proveedor_form.html', {'form': form, 'titulo': 'Nuevo proveedor'})


@login_required
@user_passes_test(admin_required)
def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    form = ProveedorForm(request.POST or None, instance=proveedor)
    if form.is_valid():
        form.save()
        messages.success(request, 'Proveedor actualizado correctamente.')
        return redirect('proveedor_list')
    return render(request, 'catalog/proveedor_form.html', {'form': form, 'titulo': 'Editar proveedor'})


@login_required
@user_passes_test(admin_required)
def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.activo = False
    proveedor.save(update_fields=['activo'])
    messages.warning(request, 'Proveedor desactivado correctamente.')
    return redirect('proveedor_list')




def admin_required(user):
    return user.is_superuser


@login_required
@user_passes_test(admin_required)
def producto_list(request):
    productos = Producto.objects.select_related(
        'categoria',
        'proveedor'
    ).all().order_by('nombre')

    q = request.GET.get('q')
    if q:
        productos = productos.filter(nombre__icontains=q)

    return render(request, 'catalog/producto_list.html', {
        'productos': productos,
        'q': q or '',
    })


@login_required
@user_passes_test(admin_required)
def producto_create(request):
    form = ProductoForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Producto creado correctamente.')
        return redirect('producto_list')

    return render(request, 'catalog/producto_form.html', {
        'form': form,
        'titulo': 'Nuevo producto'
    })


@login_required
@user_passes_test(admin_required)
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, instance=producto)

    if form.is_valid():
        form.save()
        messages.success(request, 'Producto actualizado correctamente.')
        return redirect('producto_list')

    return render(request, 'catalog/producto_form.html', {
        'form': form,
        'titulo': 'Editar producto'
    })


@login_required
@user_passes_test(admin_required)
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.activo = False
    producto.save(update_fields=['activo'])

    messages.warning(request, 'Producto desactivado correctamente.')
    return redirect('producto_list')

@login_required
@user_passes_test(admin_required)
def producto_update_inline(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre', producto.nombre)
        producto.categoria_id = request.POST.get('categoria') or None
        producto.proveedor_id = request.POST.get('proveedor') or None
        producto.origen = request.POST.get('origen', producto.origen)
        producto.precio = request.POST.get('precio', producto.precio)
        producto.iva = request.POST.get('iva', producto.iva)
        producto.unidad_medida = request.POST.get('unidad_medida', producto.unidad_medida)
        producto.pedido_minimo = request.POST.get('pedido_minimo', producto.pedido_minimo)

        producto.save()
        messages.success(request, 'Producto actualizado correctamente.')

    return redirect('producto_list')