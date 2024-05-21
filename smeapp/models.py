from django.db import models  
from django.contrib.auth.models import User  
class SizeValue(models.Model):
    SIZE_CHOICES = [
        ('MICRO', 'Micro'),
        ('SMALL', 'Small'),
        ('MEDIUM', 'Medium'),
        ('LARGE', 'Large'),
    ]
    
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.size} - {self.value}"

class Province(models.Model):
    province_name = models.CharField(max_length=100)

    def __str__(self):
        return self.province_name

class District(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=100)

    def __str__(self):
        return self.district_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    is_ward_level = models.BooleanField(default=False)
    is_district_level = models.BooleanField(default=False)
    is_province_level = models.BooleanField(default=False)
    is_national_level = models.BooleanField(default=False)

class SME(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    company = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=500)
    sector = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    age = models.IntegerField()
    type_of_business = models.CharField(max_length=100)
    product_service = models.CharField(max_length=500)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    number_of_employees = models.IntegerField()
    #size_of_business = models.ForeignKey(SizeValue, on_delete=models.CASCADE,null=True)
    asset_value= models.DecimalField(max_digits=15, decimal_places=2)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.company

class CalculationScale(models.Model):
    sme = models.ForeignKey(SME,related_name='calculation_scale', on_delete=models.CASCADE)
    size_of_employees = models.ForeignKey(SizeValue, related_name='employees_scale', on_delete=models.CASCADE, null=True)
    size_of_annual_revenue = models.ForeignKey(SizeValue, related_name='annual_revenue_scale', on_delete=models.CASCADE, null=True)
    size_of_asset_value = models.ForeignKey(SizeValue, related_name='asset_value_scale', on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(null=True)
    size_of_business = models.ForeignKey(SizeValue, related_name='business_size_scale', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Business size: {self.sme}, Rating: {self.size_of_employees}"