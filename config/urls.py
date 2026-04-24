from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from accounts.views import admin_dashboard, client_dashboard, dashboard_redirect, logout_to_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_to_login, name='logout'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    path('cliente/', client_dashboard, name='client_dashboard'),
    path('panel/', admin_dashboard, name='admin_dashboard'),
    path('cuentas/', include('accounts.urls')),
    path('catalogo/', include('catalog.urls')),
    path('pedidos/', include('orders.urls')),
    path('reportes/', include('reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
