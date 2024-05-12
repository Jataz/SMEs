# Generated by Django 5.0.3 on 2024-05-05 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smeapp', '0004_alter_sme_size_of_business'),
    ]

    operations = [
        migrations.CreateModel(
            name='SizeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('LARGE', 'Large'), ('MEDIUM', 'Medium'), ('SMALL', 'Small'), ('MICRO', 'Micro')], max_length=10)),
                ('value', models.IntegerField()),
            ],
        ),
    ]