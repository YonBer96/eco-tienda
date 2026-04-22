from django.contrib import admin

from .models import LineaPedido, OrderCycle, Pedido


class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 0


@admin.register(OrderCycle)
class OrderCycleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'inicio', 'cierre', 'cerrado')
    list_filter = ('cerrado',)
    search_fields = ('nombre',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tienda', 'usuario', 'ciclo', 'estado', 'creado_en', 'total_admin')
    list_filter = ('estado', 'ciclo', 'cliente', 'tienda')
    search_fields = ('cliente__nombre', 'tienda__nombre', 'usuario__username')
    inlines = [LineaPedidoInline]

    @admin.display(description='Total')
    def total_admin(self, obj):
        return obj.total
