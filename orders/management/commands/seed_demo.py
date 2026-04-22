from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import Cliente, Tienda
from catalog.models import CategoriaProducto, Producto, Proveedor
from orders.models import LineaPedido, OrderCycle, Pedido


PRODUCTS = [
    # Frutas
    ('Aguacate rugoso', CategoriaProducto.FRUTAS, 'kg', 'Málaga', '4.60', '4.00', 'Málaga Costa', ''),
    ('Arándanos', CategoriaProducto.FRUTAS, 'bandeja', 'Huelva', '3.30', '4.00', 'Huelva berries', ''),
    ('Kiwi verde', CategoriaProducto.FRUTAS, 'kg', 'Asturias', '5.35', '4.00', 'Asturias', ''),
    ('Limón', CategoriaProducto.FRUTAS, 'kg', 'Producción Pro', '1.80', '4.00', 'Producción Pro', ''),
    ('Manzana Fuji', CategoriaProducto.FRUTAS, 'kg', 'España', '2.60', '4.00', 'España', ''),
    ('Manzana Golden', CategoriaProducto.FRUTAS, 'kg', 'España', '2.40', '4.00', 'España', ''),
    ('Manzana Story (similar Royal)', CategoriaProducto.FRUTAS, 'kg', 'España', '2.65', '4.00', 'España', ''),
    ('Mandarina Ortanique', CategoriaProducto.FRUTAS, 'kg', 'Andalucía', '3.25', '4.00', 'Andalucía', 'Novedad'),
    ('Naranja mesa', CategoriaProducto.FRUTAS, 'kg', 'Málaga', '1.80', '4.00', 'Málaga', ''),
    ('Naranja zumo', CategoriaProducto.FRUTAS, 'kg', 'Producción Pro', '1.45', '4.00', 'Producción Pro', ''),
    ('Pera conferencia', CategoriaProducto.FRUTAS, 'kg', 'España', '3.85', '4.00', 'España', ''),
    ('Plátano', CategoriaProducto.FRUTAS, 'kg', 'Canarias', '2.80', '4.00', 'Canarias', ''),
    ('Pomelo', CategoriaProducto.FRUTAS, 'kg', 'Málaga', '1.90', '4.00', 'Málaga', ''),
    # Hortalizas
    ('Espinacas', CategoriaProducto.HORTALIZAS, 'manojo', 'Málaga', '2.40', '4.00', 'Málaga', ''),
    ('Rúcula', CategoriaProducto.HORTALIZAS, 'manojo', 'Málaga', '1.95', '4.00', 'Málaga', 'Novedad'),
    ('Lechuga maravilla', CategoriaProducto.HORTALIZAS, 'ud', 'Producción Pro', '1.50', '4.00', 'Producción Pro', 'Baja'),
    ('Lechuga trocadero', CategoriaProducto.HORTALIZAS, 'ud', 'Producción Pro', '1.50', '4.00', 'Producción Pro', 'Baja'),
    ('Hierbabuena', CategoriaProducto.HORTALIZAS, 'manojo', 'Producción Pro', '1.20', '4.00', 'Producción Pro', ''),
    ('Ajo', CategoriaProducto.HORTALIZAS, 'kg', 'Málaga', '7.20', '4.00', 'Málaga', ''),
    ('Alcachofa', CategoriaProducto.HORTALIZAS, 'kg', 'Málaga', '4.35', '4.00', 'Málaga', 'Baja'),
    ('Apio', CategoriaProducto.HORTALIZAS, 'manojo', 'Málaga', '2.00', '4.00', 'Málaga', 'Pedir por unidad'),
    ('Berenjena', CategoriaProducto.HORTALIZAS, 'kg', 'Axarquía', '3.85', '4.00', 'Axarquía', 'Baja'),
    ('Boniato', CategoriaProducto.HORTALIZAS, 'kg', 'Málaga', '2.60', '4.00', 'Málaga', 'Sube'),
    ('Brócoli', CategoriaProducto.HORTALIZAS, 'kg', 'Murcia', '4.75', '4.00', 'Murcia', 'Sube'),
    ('Calabacín', CategoriaProducto.HORTALIZAS, 'kg', 'Málaga', '2.50', '4.00', 'Málaga', 'Baja'),
    ('Calabaza cacahuete', CategoriaProducto.HORTALIZAS, 'kg', 'Málaga', '1.55', '4.00', 'Málaga', ''),
    ('Cebolla blanca', CategoriaProducto.HORTALIZAS, 'kg', 'Málaga', '1.50', '4.00', 'Málaga', ''),
    ('Cebolleta tipo calcots', CategoriaProducto.HORTALIZAS, 'manojo', 'Málaga', '2.60', '4.00', 'Málaga', ''),
    ('Champiñón portobello', CategoriaProducto.HORTALIZAS, 'kg', 'Jaén', '10.40', '4.00', 'Jaén', ''),
    ('Col verde', CategoriaProducto.HORTALIZAS, 'kg', 'Axarquía', '1.90', '4.00', 'Axarquía', 'Sube · pedir por unidad'),
    ('Coliflor blanca', CategoriaProducto.HORTALIZAS, 'ud', 'Murcia', '2.70', '4.00', 'Murcia', 'Novedad'),
    ('Coliflor colores', CategoriaProducto.HORTALIZAS, 'ud', 'Murcia', '2.85', '4.00', 'Murcia', 'Pedir por unidad'),
    ('Col lombarda', CategoriaProducto.HORTALIZAS, 'kg', 'Axarquía', '2.30', '4.00', 'Axarquía', 'Pedir por unidad'),
    ('Cúrcuma', CategoriaProducto.HORTALIZAS, 'kg', 'Exportación', '7.75', '4.00', 'Exportación', 'Sube'),
    ('Espárragos', CategoriaProducto.HORTALIZAS, 'manojo', 'Málaga', '3.55', '4.00', 'Málaga', 'Baja'),
    ('Guisantes', CategoriaProducto.HORTALIZAS, 'kg', 'Andalucía', '8.90', '4.00', 'Andalucía', 'Sube'),
    ('Jengibre', CategoriaProducto.HORTALIZAS, 'kg', 'Exportación', '5.45', '4.00', 'Exportación', ''),
    ('Judías planas', CategoriaProducto.HORTALIZAS, 'kg', 'Andalucía', '6.75', '4.00', 'Andalucía', 'Sube'),
    ('Habas', CategoriaProducto.HORTALIZAS, 'kg', 'Andalucía', '4.60', '4.00', 'Andalucía', ''),
    ('Hinojo', CategoriaProducto.HORTALIZAS, 'kg', 'Málaga', '2.20', '4.00', 'Málaga', 'Baja'),
    ('Patata blanca', CategoriaProducto.HORTALIZAS, 'kg', 'Málaga', '1.65', '4.00', 'Málaga', ''),
    ('Patata roja', CategoriaProducto.HORTALIZAS, 'kg', 'Málaga', '1.85', '4.00', 'Málaga', 'Novedad'),
    ('Pepino', CategoriaProducto.HORTALIZAS, 'kg', 'Málaga', '2.60', '4.00', 'Málaga', 'Baja'),
    ('Pimiento California rojo', CategoriaProducto.HORTALIZAS, 'kg', 'Andalucía', '6.75', '4.00', 'Andalucía', 'Novedad'),
    ('Pimiento italiano', CategoriaProducto.HORTALIZAS, 'kg', 'Andalucía', '4.05', '4.00', 'Andalucía', ''),
    ('Pimiento Palermo rojo', CategoriaProducto.HORTALIZAS, 'kg', 'Andalucía', '3.60', '4.00', 'Andalucía', 'Baja'),
    ('Puerros', CategoriaProducto.HORTALIZAS, 'kg', 'Andalucía', '2.15', '4.00', 'Andalucía', ''),
    ('Remolacha', CategoriaProducto.HORTALIZAS, 'manojo', 'Málaga', '2.10', '4.00', 'Málaga', ''),
    ('Setas shitake', CategoriaProducto.HORTALIZAS, 'kg', 'Jaén', '14.05', '4.00', 'Jaén', ''),
    ('Tomate ensalada', CategoriaProducto.HORTALIZAS, 'kg', 'Axarquía', '5.25', '4.00', 'Axarquía', ''),
    ('Tomate pera', CategoriaProducto.HORTALIZAS, 'kg', 'Andalucía', '5.25', '4.00', 'Andalucía', ''),
    ('Tomate rama', CategoriaProducto.HORTALIZAS, 'kg', 'Almería', '5.25', '4.00', 'Almería', 'Sube'),
    ('Zanahoria', CategoriaProducto.HORTALIZAS, 'kg', 'Andalucía', '1.95', '4.00', 'Andalucía', ''),
    # Envasados
    ('Aceitunas verdes bote 550 gr', CategoriaProducto.ENVASADOS, 'bote', 'Málaga', '5.40', '10.00', 'Málaga', ''),
    ('Aceitunas negras bote 550 gr', CategoriaProducto.ENVASADOS, 'bote', 'Málaga', '6.90', '10.00', 'Málaga', ''),
    ('Aceitunas verdes garrafa 1,8 kg', CategoriaProducto.ENVASADOS, 'garrafa', 'Málaga', '12.15', '10.00', 'Málaga', ''),
    ('Huevos', CategoriaProducto.ENVASADOS, 'docena', 'Málaga', '5.50', '4.00', 'Málaga', ''),
    ('Carne de membrillo 440 gr', CategoriaProducto.ENVASADOS, 'ud', 'Córdoba', '3.40', '10.00', 'Córdoba', ''),
    ('Queso fresco artesano 350 g', CategoriaProducto.ENVASADOS, 'ud', 'Málaga', '3.90', '10.00', 'Málaga', ''),
    ('Queso fresco artesano 1 kg', CategoriaProducto.ENVASADOS, 'ud', 'Málaga', '14.50', '10.00', 'Málaga', ''),
    # Frutos secos
    ('Dátil Medjoul 0,5 kg', CategoriaProducto.FRUTOS_SECOS, 'kg', 'Jordania', '8.10', '4.00', 'Jordania', ''),
    ('Dátil Medjoul 1 kg', CategoriaProducto.FRUTOS_SECOS, 'kg', 'Jordania', '14.95', '4.00', 'Jordania', ''),
    # Bebidas / almacén
    ('Leche soja Monsoy 1 litro', CategoriaProducto.BEBIDAS, 'l', 'España', '2.65', '10.00', 'España', ''),
    ('Leche avena Monsoy 1 litro', CategoriaProducto.BEBIDAS, 'l', 'España', '2.55', '10.00', 'España', ''),
    ('Leche arroz Monsoy 1 litro', CategoriaProducto.BEBIDAS, 'l', 'España', '2.60', '10.00', 'España', ''),
]


class Command(BaseCommand):
    help = 'Carga datos demo para La Foresta Agroecológica'

    @transaction.atomic
    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(username='admin')
        admin.is_superuser = True
        admin.is_staff = True
        admin.email = 'marcos@laforestaagroecologica.com'
        admin.first_name = 'Marcos'
        admin.last_name = 'Admin'
        admin.set_password('admin1234')
        admin.save()
        if created:
            self.stdout.write(self.style.SUCCESS('Superusuario demo creado: admin / admin1234'))

        demo_users = []
        for idx in range(1, 6):
            username = f'cliente{idx}'
            user, _ = User.objects.get_or_create(username=username)
            user.email = f'{username}@laforestaagroecologica.local'
            user.first_name = f'Cliente {idx}'
            user.last_name = 'Demo'
            user.set_password('cliente1234')
            user.save()
            demo_users.append(user)

        proveedores_data = [
            ('Producción Pro', 'Equipo compras', 'compras@produccionpro.local'),
            ('Málaga Costa', 'María López', 'pedidos@malagacosta.local'),
            ('Andalucía Fresh', 'Antonio García', 'pedidos@andaluciafresh.local'),
            ('Eco Axarquía', 'Lucía Martín', 'pedidos@ecoaxarquia.local'),
            ('Distribuciones Sierra', 'Javier Ruiz', 'pedidos@distsierra.local'),
        ]
        proveedores = []
        for idx, (nombre, contacto, email) in enumerate(proveedores_data, start=1):
            proveedor, _ = Proveedor.objects.get_or_create(nombre=nombre)
            proveedor.contacto = contacto
            proveedor.telefono = f'600123{idx:03d}'
            proveedor.email = email
            proveedor.direccion = f'Proveedor demo {idx}'
            proveedor.activo = True
            proveedor.save()
            proveedores.append(proveedor)

        categorias = {nombre: CategoriaProducto.objects.get_or_create(nombre=nombre)[0] for nombre in CategoriaProducto.NOMBRES_PREDETERMINADOS}

        provider_lookup = {
            'Málaga': proveedores[1],
            'Málaga Costa': proveedores[1],
            'Andalucía': proveedores[2],
            'Axarquía': proveedores[3],
            'Producción Pro': proveedores[0],
            'España': proveedores[4],
            'Murcia': proveedores[4],
            'Jaén': proveedores[4],
            'Jordania': proveedores[4],
            'Canarias': proveedores[4],
            'Asturias': proveedores[4],
            'Huelva': proveedores[4],
            'Almería': proveedores[2],
            'Córdoba': proveedores[4],
            'Exportación': proveedores[4],
        }
        default_provider = proveedores[4]

        created_products = []
        for orden, (nombre, categoria_nombre, unidad, origen, precio, iva, provider_key, observacion) in enumerate(PRODUCTS, start=1):
            provider = provider_lookup.get(provider_key, default_provider)
            producto, _ = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'categoria': categorias[categoria_nombre],
                    'proveedor': provider,
                    'precio': Decimal(precio),
                    'iva': Decimal(iva),
                    'unidad_medida': unidad,
                    'pedido_minimo': Decimal('0.50') if unidad == 'kg' else Decimal('1.00'),
                    'incremento_pedido': Decimal('0.50') if unidad == 'kg' else Decimal('1.00'),
                    'stock_disponible': Decimal('999.00'),
                    'descripcion': observacion,
                    'orden': orden,
                    'formato_caja': Decimal('5.00') if unidad == 'kg' else None,
                    'origen': origen,
                    'activo': True,
                },
            )
            producto.categoria = categorias[categoria_nombre]
            producto.proveedor = provider
            producto.precio = Decimal(precio)
            producto.iva = Decimal(iva)
            producto.unidad_medida = unidad
            producto.pedido_minimo = Decimal('0.50') if unidad == 'kg' else Decimal('1.00')
            producto.incremento_pedido = Decimal('0.50') if unidad == 'kg' else Decimal('1.00')
            producto.stock_disponible = Decimal('999.00')
            producto.descripcion = observacion
            producto.orden = orden
            producto.formato_caja = Decimal('5.00') if unidad == 'kg' else None
            producto.origen = origen
            producto.activo = True
            producto.save()
            created_products.append(producto)

        clientes = []
        tiendas = []
        for idx, user in enumerate(demo_users, start=1):
            cliente, _ = Cliente.objects.get_or_create(nombre=f'Cliente Demo {idx}')
            cliente.telefono = f'6111111{idx:02d}'
            cliente.email = f'compras{idx}@cliente-demo.local'
            cliente.direccion = f'Calle Demo {idx}'
            if hasattr(cliente, 'nif'):
                cliente.nif = f'B10{idx:06d}'
            if hasattr(cliente, 'direccion_facturacion'):
                cliente.direccion_facturacion = f'Avenida Facturación {idx}'
            cliente.save()
            cliente.usuarios.add(user)
            clientes.append(cliente)
            for sufijo in ('Centro', 'Mercado'):
                tienda, _ = Tienda.objects.get_or_create(cliente=cliente, nombre=f'Tienda {sufijo} {idx}')
                tienda.direccion = f'Zona {sufijo} {idx}'
                tienda.telefono = f'6222222{idx:02d}'
                tienda.email = f'tienda-{sufijo.lower()}-{idx}@cliente-demo.local'
                if hasattr(tienda, 'direccion_facturacion'):
                    tienda.direccion_facturacion = f'Zona {sufijo} {idx} · Facturación'
                tienda.save()
                tiendas.append(tienda)

        now = timezone.localtime()
        monday = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_cycle = monday + timedelta(days=3, hours=14)  # jueves 14:00
        end_of_cycle = monday + timedelta(days=5, hours=20)    # sábado 20:00
        cycle_name = f'Semana {start_of_cycle:%Y-%m-%d} / {end_of_cycle:%Y-%m-%d}'
        ciclo, _ = OrderCycle.objects.get_or_create(
            nombre=cycle_name,
            defaults={
                'inicio': start_of_cycle,
                'cierre': end_of_cycle,
                'reparto_inicio': end_of_cycle + timedelta(hours=10),
                'reparto_fin': end_of_cycle + timedelta(days=1, hours=14),
                'cerrado': False,
            },
        )
        ciclo.inicio = start_of_cycle
        ciclo.cierre = end_of_cycle
        ciclo.reparto_inicio = end_of_cycle + timedelta(hours=10)
        ciclo.reparto_fin = end_of_cycle + timedelta(days=1, hours=14)
        ciclo.cerrado = False
        ciclo.save()
        OrderCycle.objects.exclude(pk=ciclo.pk).update(cerrado=True)

        selection_indexes = [0, 3, 7, 12, 16, 20, 24, 28, 33, 37, 42, 46, 50, 55, 59, 63]
        for idx, tienda in enumerate(tiendas[:10], start=1):
            cliente = tienda.cliente
            usuario = cliente.usuarios.first() or demo_users[(idx - 1) % len(demo_users)]
            pedido, _ = Pedido.objects.get_or_create(
                ciclo=ciclo,
                tienda=tienda,
                defaults={
                    'usuario': usuario,
                    'cliente': cliente,
                    'estado': Pedido.CONFIRMADO,
                    'observaciones': f'Pedido demo {idx} para revisión comercial',
                },
            )
            pedido.usuario = usuario
            pedido.cliente = cliente
            pedido.estado = Pedido.CONFIRMADO
            pedido.observaciones = f'Pedido demo {idx} para revisión comercial'
            pedido.save()
            pedido.lineas.all().delete()

            base_index = selection_indexes[idx % len(selection_indexes)]
            for offset in range(5):
                producto = created_products[(base_index + offset * 2) % len(created_products)]
                cantidad = Decimal(str((idx % 3) + offset + 1))
                if producto.unidad_medida == 'kg':
                    cantidad += Decimal('0.50')
                LineaPedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    proveedor_snapshot=producto.proveedor,
                    nombre_producto_snapshot=producto.nombre,
                    unidad_medida_snapshot=producto.unidad_medida,
                    precio_unitario_snapshot=producto.precio,
                    iva_snapshot=producto.iva,
                    cantidad=cantidad,
                )

        self.stdout.write(self.style.SUCCESS(f'Datos demo cargados: {len(created_products)} productos y 10 pedidos confirmados.'))
