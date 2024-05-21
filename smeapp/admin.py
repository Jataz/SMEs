from django.contrib import admin
from .models import SME, District, Province, SizeValue, CalculationScale, UserProfile
from django.contrib.auth.models import Permission
from django import forms

class SMEAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'company', 'contact_person', 'phone_number',
        'province', 'district', 'address', 'sector','email',
        'type_of_business', 'product_service', 'annual_revenue',
        'number_of_employees', 'asset_value'
    )

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content_type', 'codename') # Register Province model normally
    
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'province', 'district_name')

class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'size', 'value')

class CalculationScaleAdmin(admin.ModelAdmin):
    list_display = ('sme', 'size_of_employees', 'size_of_annual_revenue', 'size_of_asset_value', 'rating', 'size_of_business')
    list_filter = ('sme', 'size_of_business')  # Optionally add filters for easier navigation
    search_fields = ('sme__name', 'size_of_business')  # Optionally add search functionality 
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'province', 'district','is_ward_level','is_district_level','is_province_level','is_national_level')
       
admin.site.register(SizeValue,SizeAdmin)
admin.site.register(Province)
admin.site.register(District, DistrictAdmin)
admin.site.register(SME, SMEAdmin)
admin.site.register(CalculationScale,CalculationScaleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)