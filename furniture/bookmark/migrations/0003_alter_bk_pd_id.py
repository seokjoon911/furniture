# Generated by Django 4.2.14 on 2024-08-20 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_image'),
        ('bookmark', '0002_alter_bk_pd_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bk',
            name='pd_id',
            field=models.ManyToManyField(to='product.product', verbose_name='Products'),
        ),
    ]
