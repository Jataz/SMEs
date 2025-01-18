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
    province = models.ForeignKey(Province, on_delete=models.CASCADE,related_name='districts')
    district_name = models.CharField(max_length=100)

    def __str__(self):
        return self.district_name

class Ward(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE,related_name='wards')
    ward_name = models.CharField(max_length=100)

    def __str__(self):
        return self.ward_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    ward = models.ForeignKey(Ward,on_delete=models.SET_NULL, null=True, blank=True)
    is_ward_level = models.BooleanField(default=False)
    is_district_level = models.BooleanField(default=False)
    is_province_level = models.BooleanField(default=False)
    is_national_level = models.BooleanField(default=False)

class SME(models.Model):
    sme_ref_number = models.CharField(unique=True)
    company = models.CharField()
    contact_person = models.CharField(unique=True)
    phone_number = models.CharField(unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField()
    sector = models.ForeignKey('Sector', on_delete=models.CASCADE,default=1) 
    sex = models.CharField()
    age = models.CharField()
    disability = models.CharField()
    type_of_business = models.CharField()
    product_service = models.CharField()
    compliance = models.CharField(max_length=255, default="ZIMRA")
    registration = models.CharField(max_length=255,default="Registered")
    tax = models.CharField(max_length=255, default="Presumptive Tax")
    training = models.CharField(max_length=255, default="Received Training")
    education = models.CharField(max_length=255, default="Received Education")
    export = models.CharField()
    comments = models.CharField()
    number_of_employees = models.IntegerField()
    asset_value = models.DecimalField(max_digits=20, decimal_places=2)
    annual_revenue = models.DecimalField(max_digits=20, decimal_places=2)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
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

class Sector(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Sector name (e.g., Agriculture, Mining)

    def __str__(self):
        return self.name


class SectorThreshold(models.Model):

    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="thresholds")
    size = models.ForeignKey(SizeValue, on_delete=models.CASCADE, related_name='sector_thresholds')  # Link to SizeValue
    max_employees = models.IntegerField()  # Maximum number of employees for this size
    max_annual_revenue = models.FloatField()  # Maximum annual revenue for this size
    max_asset_value = models.FloatField()  # Maximum asset value for this size

    class Meta:
        unique_together = ('sector', 'size')  # Ensure no duplicate thresholds for the same sector and size

    def __str__(self):
        return f"{self.sector.name} - {self.size}"