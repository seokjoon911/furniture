# Generated by Django 4.2.14 on 2024-09-07 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]
