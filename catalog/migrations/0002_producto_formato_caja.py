from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='formato_caja',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Cantidad por caja para pedir al proveedor. Ejemplo: 5 kg o 5 ud por caja.', max_digits=10, null=True),
        ),
    ]
