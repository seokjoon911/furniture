# Generated by Django 4.2.14 on 2024-08-23 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prod_id',
            field=models.CharField(default='68d82a80-86a6-46c9-900f-cad7b9cc06fc', editable=False, max_length=36, primary_key=True, serialize=False),
        ),
    ]