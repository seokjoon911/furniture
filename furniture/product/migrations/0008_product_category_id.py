# Generated by Django 4.2.14 on 2024-09-19 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
        ('product', '0007_product_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category_id',
            field=models.ForeignKey(db_column='category_id', default=1, on_delete=django.db.models.deletion.CASCADE, to='menu.subcategory'),
            preserve_default=False,
        ),
    ]
