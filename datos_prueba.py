from catalog.models import Proveedor

proveedores = [
    {
        "nombre": "Makro",
        "email": "pedidos@makro.es",
        "telefono": "900100200",
    },
    {
        "nombre": "Distribuciones Sierra",
        "email": "ventas@distribucionessierra.es",
        "telefono": "954111222",
    },
    {
        "nombre": "Málaga Costa",
        "email": "info@malagacosta.es",
        "telefono": "952333444",
    },
    {
        "nombre": "Frutas del Sur",
        "email": "pedidos@frutasdelsur.es",
        "telefono": "955666777",
    },
]

for data in proveedores:
    proveedor, creado = Proveedor.objects.get_or_create(
        nombre=data["nombre"],
        defaults={
            "email": data["email"],
            "telefono": data["telefono"],
        }
    )

    if creado:
        print(f"Creado: {proveedor.nombre}")
    else:
        print(f"Ya existe: {proveedor.nombre}")