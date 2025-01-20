# Generated by Django 5.1 on 2025-01-20 16:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_alter_supply_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='combo',
            name='products',
        ),
        migrations.AlterField(
            model_name='productsincombo',
            name='combo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='storage.combo'),
        ),
        migrations.AlterField(
            model_name='productsincombo',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='combos', to='storage.product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='supply',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Количество'),
        ),
    ]
