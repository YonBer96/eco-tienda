from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='direccion_facturacion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='tienda',
            name='direccion_facturacion',
            field=models.TextField(blank=True),
        ),
    ]
