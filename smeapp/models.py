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
    
class Sector(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Sector name (e.g., Agriculture, Mining)

    def __str__(self):
        return self.name
class SME(models.Model):
    FORM_OF_BUSINESS_CHOICES = [
        ("Private Limited", "Private Limited"),
        ("Private Business Cooperation", "Private Business Cooperation"),
        ("Cooperative", "Cooperative"),
        ("Partnership", "Partnership"),
        ("Syndicate", "Syndicate"),
        ("Consortium", "Consortium"),
        ("Group", "Group"),
        ("Sole Proprietorship", "Sole Proprietorship"),
    ]

    REGISTRATION_STATUS_CHOICES = [
        ("Registered", "Registered"),
        ("Not-Registered", "Not Registered"),
    ]

    EXPORT_STATUS_CHOICES = [
        ("Exporter", "Exporter"),
        ("Non-Exporter", "Non-Exporter"),
    ]

    COMPLIANCE_STATUS_CHOICES = [
        ("Compliant", "Compliant"),
        ("Non-Compliant", "Non-Compliant"),
    ]

    OWNERSHIP_CHOICES = [
        ("Youth owned", "Youth owned"),
        ("Women Owned", "Women Owned"),
        ("Men Owned", "Men Owned"),
        ("Warvets Owned", "Warvets Owned"),
        ("Disabled Owned", "Disabled Owned"),
    ]

    EDUCATION_LEVEL_CHOICES = [
        ("Primary", "Primary"),
        ("O Level", "O Level"),
        ("A Level", "A Level"),
        ("Tertiary", "Tertiary"),
        ("None", "None"),
    ]

    SOURCE_OF_FUNDS_CHOICES = [
        ("Government loan", "Government loan"),
        ("Venture capital", "Venture capital"),
        ("Own savings", "Own savings"),
    ]
    
    # === Identification ===
    sme_ref_number = models.CharField(max_length=255, unique=True)

    # Main business fields
    company = models.CharField(max_length=255)
    type_of_business = models.CharField(max_length=50, choices=FORM_OF_BUSINESS_CHOICES)
    registration = models.CharField(max_length=20, choices=REGISTRATION_STATUS_CHOICES)
    sector = models.CharField(max_length=100)
    product_service = models.CharField(max_length=255)
    number_of_employees = models.PositiveIntegerField()
    export = models.CharField(max_length=20, choices=EXPORT_STATUS_CHOICES)
    ownership = models.CharField(max_length=30, choices=OWNERSHIP_CHOICES, blank=True, null=True)

    # Contact information
    contact_person = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    education = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, blank=True, null=True)

    # Business Support
    support_service = models.JSONField(blank=True, null=True)  # Store multiple selected services as a list
    training_received = models.CharField(max_length=255, blank=True, null=True)
    funding_received = models.CharField(max_length=255, blank=True, null=True)

    # Compliance Section
    compliance = models.CharField(max_length=255)
    tax = models.CharField(max_length=100)

    # Financial Info
    source_of_funds = models.CharField(max_length=30, choices=SOURCE_OF_FUNDS_CHOICES, blank=True, null=True)
    annual_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    asset_value = models.DecimalField(max_digits=12, decimal_places=2)

    # Challenges
    comments = models.TextField(blank=True, null=True)
    
    # === Geographical Info ===
    sector = models.ForeignKey('Sector', on_delete=models.CASCADE)
    province = models.ForeignKey('Province', on_delete=models.CASCADE)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    ward = models.ForeignKey('Ward', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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