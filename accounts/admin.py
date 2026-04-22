from django.contrib import admin

from .models import Cliente, PerfilUsuario, Tienda


class TiendaInline(admin.TabularInline):
    model = Tienda
    extra = 1


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'nif', 'email')
    filter_horizontal = ('usuarios',)
    inlines = [TiendaInline]


@admin.register(Tienda)
class TiendaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cliente', 'telefono', 'email', 'activa')
    list_filter = ('activa', 'cliente')
    search_fields = ('nombre', 'cliente__nombre')


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono')
    search_fields = ('user__username', 'user__email')
