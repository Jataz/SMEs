# Generated by Django 5.0.3 on 2024-05-21 19:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smeapp', '0003_sme_created_at_sme_updated_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ward_name', models.CharField(max_length=100)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smeapp.district')),
            ],
        ),
    ]
