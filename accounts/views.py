from django.contrib import messages
from django.contrib.auth import logout
<<<<<<< HEAD
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from orders.models import Pedido

from .forms import (
    ClienteCreateForm,
    ClienteForm,
    ProfileUpdateForm,
    TiendaForm,
    UserUpdateForm,
)
from .models import Cliente, Tienda
=======
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from orders.models import Pedido
from .models import Cliente

from .forms import ProfileUpdateForm, UserUpdateForm

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from .models import Cliente, Tienda
from .forms import ClienteForm, TiendaForm
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e


@login_required
def dashboard_redirect(request):
    return redirect('admin_dashboard' if request.user.is_superuser else 'client_dashboard')


@login_required
def client_dashboard(request):
    pedidos = Pedido.objects.filter(usuario=request.user).select_related('cliente', 'tienda', 'ciclo')[:8]
    return render(request, 'accounts/client_dashboard.html', {'pedidos': pedidos})


@login_required
def admin_dashboard(request):
    stats = {
        'pedidos': Pedido.objects.count(),
        'pedidos_confirmados': Pedido.objects.filter(estado=Pedido.CONFIRMADO).count(),
        'clientes': Cliente.objects.count(),
<<<<<<< HEAD
        'tiendas': Tienda.objects.count(),
=======
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e
    }
    ultimos_pedidos = Pedido.objects.select_related('cliente', 'tienda', 'usuario').order_by('-creado_en')[:10]
    return render(request, 'accounts/admin_dashboard.html', {'stats': stats, 'ultimos_pedidos': ultimos_pedidos})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.perfil)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Tus datos se han actualizado correctamente.')
            return redirect('profile_edit')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.perfil)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def logout_to_login(request):
    logout(request)
    return redirect('login')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('profile_edit')

    def form_valid(self, form):
        messages.success(self.request, 'La contraseña se ha cambiado correctamente.')
        return super().form_valid(form)

<<<<<<< HEAD

=======
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e
def admin_required(user):
    return user.is_superuser


@login_required
@user_passes_test(admin_required)
def cliente_list(request):
<<<<<<< HEAD
    clientes = Cliente.objects.prefetch_related('tiendas', 'usuarios').all()
=======
    clientes = Cliente.objects.all()
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e
    return render(request, 'accounts/cliente_list.html', {'clientes': clientes})


@login_required
@user_passes_test(admin_required)
def cliente_create(request):
<<<<<<< HEAD
    form = ClienteCreateForm(request.POST or None)

    if form.is_valid():
        cliente = form.save()
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        cliente.usuarios.add(user)
        messages.success(request, 'Cliente y usuario de acceso creados correctamente.')
        return redirect('cliente_list')

    return render(request, 'accounts/cliente_form.html', {
        'form': form,
        'titulo': 'Nuevo cliente',
        'modo_creacion': True,
    })
=======
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente creado correctamente.')
        return redirect('cliente_list')
    return render(request, 'accounts/cliente_form.html', {'form': form, 'titulo': 'Nuevo cliente'})
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e


@login_required
@user_passes_test(admin_required)
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
<<<<<<< HEAD

=======
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente actualizado correctamente.')
        return redirect('cliente_list')
<<<<<<< HEAD

    return render(request, 'accounts/cliente_form.html', {
        'form': form,
        'titulo': 'Editar cliente',
        'modo_creacion': False,
    })
=======
    return render(request, 'accounts/cliente_form.html', {'form': form, 'titulo': 'Editar cliente'})
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e


@login_required
@user_passes_test(admin_required)
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.activo = False
    cliente.save(update_fields=['activo'])
    messages.warning(request, 'Cliente desactivado correctamente.')
<<<<<<< HEAD
    return redirect('cliente_list')


@login_required
@user_passes_test(admin_required)
def tienda_list(request):
    tiendas = Tienda.objects.select_related('cliente').all()
    return render(request, 'accounts/tienda_list.html', {'tiendas': tiendas})


@login_required
@user_passes_test(admin_required)
def tienda_create(request):
    form = TiendaForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Tienda creada correctamente.')
        return redirect('tienda_list')

    return render(request, 'accounts/tienda_form.html', {
        'form': form,
        'titulo': 'Nueva tienda',
    })


@login_required
@user_passes_test(admin_required)
def tienda_update(request, pk):
    tienda = get_object_or_404(Tienda, pk=pk)
    form = TiendaForm(request.POST or None, instance=tienda)

    if form.is_valid():
        form.save()
        messages.success(request, 'Tienda actualizada correctamente.')
        return redirect('tienda_list')

    return render(request, 'accounts/tienda_form.html', {
        'form': form,
        'titulo': 'Editar tienda',
    })


@login_required
@user_passes_test(admin_required)
def tienda_delete(request, pk):
    tienda = get_object_or_404(Tienda, pk=pk)
    tienda.activa = False
    tienda.save(update_fields=['activa'])
    messages.warning(request, 'Tienda desactivada correctamente.')
    return redirect('tienda_list')
=======
    return redirect('cliente_list')
>>>>>>> 45f9c18fbb29f537da3f8aac6bda6a0f91f3283e
