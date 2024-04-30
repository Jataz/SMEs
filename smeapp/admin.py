from django.contrib import admin
from .models import SME
from django.contrib.auth.models import Permission

class SMEdmin(admin.ModelAdmin):
    list_display = (
        'id', 'company', 'contact_person', 'phone_number',
        'province', 'district', 'address', 'sector','email',
        'type_of_business', 'product_service', 'annual_revenue',
        'number_of_employees', 'asset_value', 'size_of_business'
    )

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content_type', 'codename')

admin.site.register(SME, SMEdmin)
admin.site.register(Permission, PermissionAdmin)