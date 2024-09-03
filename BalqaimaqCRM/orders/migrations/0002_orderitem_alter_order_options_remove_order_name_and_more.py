# Generated by Django 5.1 on 2024-08-31 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_client_is_active'),
        ('orders', '0001_initial'),
        ('storage', '0002_alter_product_amount_alter_product_cost_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Количество')),
            ],
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['-created_at'], name='orders_orde_created_f0ce29_idx'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='storage.product'),
        ),
    ]
