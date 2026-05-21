from django.db import migrations


def split_categories(apps, schema_editor):
    CategoriaProducto = apps.get_model('catalog', 'CategoriaProducto')
    Producto = apps.get_model('catalog', 'Producto')

    frutas, _ = CategoriaProducto.objects.get_or_create(nombre='Frutas')
    hortalizas, _ = CategoriaProducto.objects.get_or_create(nombre='Hortalizas')
    CategoriaProducto.objects.get_or_create(nombre='Envasados')
    CategoriaProducto.objects.get_or_create(nombre='Frutos secos')
    CategoriaProducto.objects.get_or_create(nombre='Bebidas')

    category = CategoriaProducto.objects.filter(nombre='Frutas y hortalizas').first()
    if category:
        frutas_keywords = ['manzana', 'naranja', 'pera', 'plátano', 'platano', 'uva', 'melón', 'melon', 'sandía', 'sandia', 'mandarina', 'limón', 'limon', 'kiwi', 'fresa', 'melocotón', 'melocoton']
        for producto in Producto.objects.filter(categoria=category):
            nombre = (producto.nombre or '').lower()
            destino = frutas if any(k in nombre for k in frutas_keywords) else hortalizas
            producto.categoria = destino
            producto.save(update_fields=['categoria'])
        category.delete()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_producto_origen_y_categorias'),
    ]

    operations = [
        migrations.RunPython(split_categories, noop),
    ]
