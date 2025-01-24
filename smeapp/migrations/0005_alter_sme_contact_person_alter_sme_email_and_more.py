# Generated by Django 5.0.3 on 2025-01-24 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smeapp', '0004_alter_sme_compliance_alter_sme_education_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sme',
            name='contact_person',
            field=models.CharField(error_messages={'unique': 'This contact person already exists. Please use a different name.'}, unique=True),
        ),
        migrations.AlterField(
            model_name='sme',
            name='email',
            field=models.EmailField(error_messages={'unique': 'This email is already registered. Please use a different email address.'}, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='sme',
            name='phone_number',
            field=models.CharField(error_messages={'unique': 'This phone number is already registered. Please use a different number.'}, max_length=20, unique=True),
        ),
    ]
