from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_producto_formato_caja'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='iva',
            field=models.DecimalField(choices=[(Decimal('4.00'), '4%'), (Decimal('10.00'), '10%')], decimal_places=2, default=Decimal('4.00'), max_digits=4),
        ),
        migrations.AddField(
            model_name='producto',
            name='pedido_minimo',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AddField(
            model_name='producto',
            name='incremento_pedido',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.50'), max_digits=10),
        ),
        migrations.AddField(
            model_name='producto',
            name='limitar_stock',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='producto',
            name='unidad_medida',
            field=models.CharField(choices=[('kg', 'Kilogramo'), ('ud', 'Unidad'), ('docena', 'Docena'), ('l', 'Litro'), ('manojo', 'Manojo'), ('caja', 'Caja')], default='kg', max_length=20),
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'ordering': ['nombre']},
        ),
    ]
