# marcos_shop

Aplicación Django para gestión de pedidos semanales de productos agrícolas.

## Características

- Inicio de sesión obligatorio.
- Los usuarios solo pueden ser creados, editados o eliminados por el superusuario.
- Clientes con varias tiendas.
- Catálogo de productos en formato tabla, sin imágenes.
- Demo de cierre de tienda visible los lunes hasta las 17:00.
- Resumen dinámico de compra en la misma pantalla.
- Gestión de proveedores, productos, clientes y pedidos.
- Albarán individual PDF por pedido.
- Albarán general semanal con cantidades agregadas.
- Albarán semanal agrupado por proveedor respetando el proveedor guardado en cada pedido.
- Envío opcional del albarán por correo.
- Seed demo ampliado con 5 usuarios, 5 proveedores, 10 productos, 10 pedidos y 5 clientes.

## Instalación

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Base de datos

Por defecto usa SQLite para facilitar pruebas. Si quieres PostgreSQL, cambia `DATABASES` en `config/settings.py`.

## Primer arranque

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

## Credenciales demo

- Admin: `admin / admin1234`
- Clientes demo: `cliente1..cliente5 / cliente1234`

## Flujo recomendado

1. Entrar con superusuario.
2. Revisar productos y, si hace falta, cambiar proveedor, precio o unidad desde `/admin/catalog/producto/`.
3. Crear o editar pedidos de la semana.
4. Descargar los tres albaranes desde el detalle del pedido o desde los resúmenes de administración.

## Notas

- Los pedidos antiguos guardan snapshots de precio, proveedor, unidad y nombre del producto.
- Un pedido confirmado sigue siendo editable mientras el ciclo esté abierto.
- Si un proveedor cambia a mitad de semana, los albaranes por proveedor respetan el proveedor guardado en cada línea del pedido en el momento de confirmación/edición.
