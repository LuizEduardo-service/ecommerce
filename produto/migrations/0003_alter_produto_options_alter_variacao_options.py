# Generated by Django 5.0.2 on 2024-02-19 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0002_variacao'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produto',
            options={'verbose_name': 'Produto', 'verbose_name_plural': 'Produtos'},
        ),
        migrations.AlterModelOptions(
            name='variacao',
            options={'verbose_name': 'Variação', 'verbose_name_plural': 'Variações'},
        ),
    ]
