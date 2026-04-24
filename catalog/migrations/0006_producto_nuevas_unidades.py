from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_split_frutas_hortalizas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='unidad_medida',
            field=models.CharField(
                choices=[
                    ('kg', 'Kilogramo'),
                    ('ud', 'Unidad'),
                    ('docena', 'Docena'),
                    ('l', 'Litro'),
                    ('manojo', 'Manojo'),
                    ('caja', 'Caja'),
                    ('bandeja', 'Bandeja'),
                    ('bote', 'Bote'),
                    ('garrafa', 'Garrafa'),
                ],
                default='kg',
                max_length=20,
            ),
        ),
    ]
