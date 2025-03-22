# Generated by Django 5.0.3 on 2025-03-22 11:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SizeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('MICRO', 'Micro'), ('SMALL', 'Small'), ('MEDIUM', 'Medium'), ('LARGE', 'Large')], max_length=10)),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district_name', models.CharField(max_length=100)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='smeapp.province')),
            ],
        ),
        migrations.CreateModel(
            name='SME',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sme_ref_number', models.CharField(max_length=255, unique=True)),
                ('company', models.CharField(max_length=255)),
                ('type_of_business', models.CharField(choices=[('Private Limited', 'Private Limited'), ('Private Business Cooperation', 'Private Business Cooperation'), ('Cooperative', 'Cooperative'), ('Partnership', 'Partnership'), ('Syndicate', 'Syndicate'), ('Consortium', 'Consortium'), ('Group', 'Group'), ('Sole Proprietorship', 'Sole Proprietorship')], max_length=50)),
                ('registration', models.CharField(choices=[('Registered', 'Registered'), ('Not-Registered', 'Not Registered')], max_length=20)),
                ('product_service', models.CharField(max_length=255)),
                ('number_of_employees', models.PositiveIntegerField()),
                ('export', models.CharField(choices=[('Exporter', 'Exporter'), ('Non-Exporter', 'Non-Exporter')], max_length=20)),
                ('ownership', models.CharField(blank=True, choices=[('Youth owned', 'Youth owned'), ('Women Owned', 'Women Owned'), ('Men Owned', 'Men Owned'), ('Warvets Owned', 'Warvets Owned'), ('Disabled Owned', 'Disabled Owned')], max_length=30, null=True)),
                ('contact_person', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('education', models.CharField(blank=True, choices=[('Primary', 'Primary'), ('O Level', 'O Level'), ('A Level', 'A Level'), ('Tertiary', 'Tertiary'), ('None', 'None')], max_length=20, null=True)),
                ('support_service', models.JSONField(blank=True, null=True)),
                ('training_received', models.CharField(blank=True, max_length=255, null=True)),
                ('funding_received', models.CharField(blank=True, max_length=255, null=True)),
                ('compliance', models.CharField(max_length=255)),
                ('tax', models.CharField(max_length=100)),
                ('source_of_funds', models.CharField(blank=True, choices=[('Government loan', 'Government loan'), ('Venture capital', 'Venture capital'), ('Own savings', 'Own savings')], max_length=30, null=True)),
                ('annual_revenue', models.DecimalField(decimal_places=2, max_digits=12)),
                ('asset_value', models.DecimalField(decimal_places=2, max_digits=12)),
                ('comments', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smeapp.district')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smeapp.province')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smeapp.sector')),
            ],
        ),
        migrations.CreateModel(
            name='CalculationScale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(null=True)),
                ('size_of_annual_revenue', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='annual_revenue_scale', to='smeapp.sizevalue')),
                ('size_of_asset_value', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asset_value_scale', to='smeapp.sizevalue')),
                ('size_of_business', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='business_size_scale', to='smeapp.sizevalue')),
                ('size_of_employees', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees_scale', to='smeapp.sizevalue')),
                ('sme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calculation_scale', to='smeapp.sme')),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ward_name', models.CharField(max_length=100)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wards', to='smeapp.district')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ward_level', models.BooleanField(default=False)),
                ('is_district_level', models.BooleanField(default=False)),
                ('is_province_level', models.BooleanField(default=False)),
                ('is_national_level', models.BooleanField(default=False)),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='smeapp.district')),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='smeapp.province')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='smeapp.ward')),
            ],
        ),
        migrations.AddField(
            model_name='sme',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smeapp.ward'),
        ),
        migrations.CreateModel(
            name='SectorThreshold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_employees', models.IntegerField()),
                ('max_annual_revenue', models.FloatField()),
                ('max_asset_value', models.FloatField()),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thresholds', to='smeapp.sector')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sector_thresholds', to='smeapp.sizevalue')),
            ],
            options={
                'unique_together': {('sector', 'size')},
            },
        ),
    ]
