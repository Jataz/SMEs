# Generated by Django 5.0.3 on 2024-05-12 20:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smeapp', '0011_calculationscale_delete_scalebusiness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculationscale',
            name='rating',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratio', to='smeapp.sizevalue'),
        ),
    ]
