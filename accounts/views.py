from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from orders.models import Pedido
from .models import Cliente

from .forms import ProfileUpdateForm, UserUpdateForm


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
