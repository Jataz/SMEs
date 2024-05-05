from django.contrib import admin
from .models import SME, District, Province, SizeValue
from django.contrib.auth.models import Permission
from django import forms

class SMEAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'company', 'contact_person', 'phone_number',
        'province', 'district', 'address', 'sector','email',
        'type_of_business', 'product_service', 'annual_revenue',
        'number_of_employees', 'asset_value', 'size_of_business'
    )

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content_type', 'codename') # Register Province model normally
    
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'province', 'district_name')

class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'size', 'value')
    
admin.site.register(SizeValue,SizeAdmin)
admin.site.register(Province)
admin.site.register(District, DistrictAdmin)
admin.site.register(SME, SMEAdmin)
admin.site.register(Permission, PermissionAdmin)