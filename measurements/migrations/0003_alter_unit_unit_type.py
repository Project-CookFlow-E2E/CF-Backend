# Generated by Django 5.2.3 on 2025-06-13 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0002_unit_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='unit_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='measurements.unittype'),
        ),
    ]
