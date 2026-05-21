from django.db import migrations, models


def create_default_categories(apps, schema_editor):
    CategoriaProducto = apps.get_model('catalog', 'CategoriaProducto')
    Producto = apps.get_model('catalog', 'Producto')

    default_names = [
        'Frutas y hortalizas',
        'Envasados',
        'Frutos secos',
        'Bebidas',
    ]

    categories = {name: CategoriaProducto.objects.get_or_create(nombre=name)[0] for name in default_names}

    mapping = {
        'Fruta': 'Frutas y hortalizas',
        'Frutas': 'Frutas y hortalizas',
        'Verdura': 'Frutas y hortalizas',
        'Verduras': 'Frutas y hortalizas',
        'Hortaliza': 'Frutas y hortalizas',
        'Hortalizas': 'Frutas y hortalizas',
        'Lácteos': 'Envasados',
        'Huevos': 'Envasados',
        'Otros': 'Envasados',
    }

    for old_name, new_name in mapping.items():
        old = CategoriaProducto.objects.filter(nombre=old_name).first()
        if not old:
            continue
        Producto.objects.filter(categoria=old).update(categoria=categories[new_name])
        old.delete()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_producto_iva_y_configuracion'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='origen',
            field=models.CharField(blank=True, help_text='Origen o procedencia del producto. Ejemplo: Huelva, Valencia, cooperativa local, etc.', max_length=150),
        ),
        migrations.RunPython(create_default_categories, noop),
    ]
