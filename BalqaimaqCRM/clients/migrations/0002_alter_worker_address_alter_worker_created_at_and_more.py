# Generated by Django 5.1 on 2025-01-18 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='address',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='worker',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
    ]
