from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineapedido',
            name='iva_snapshot',
            field=models.DecimalField(decimal_places=2, default=Decimal('4.00'), max_digits=4),
        ),
    ]
