# Generated by Django 4.2.14 on 2024-08-23 23:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark', '0004_alter_bk_bk_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bk',
            name='bk_no',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False),
        ),
    ]
