from django.db import models    
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

class SME(models.Model):
    company = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=500)
    sector = models.CharField(max_length=100)
    type_of_business = models.CharField(max_length=100)
    product_service = models.CharField(max_length=500)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    number_of_employees = models.IntegerField()
    size_of_business = models.ForeignKey(SizeValue, on_delete=models.CASCADE,null=True)
    asset_value= models.DecimalField(max_digits=15, decimal_places=2)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.company

class ScaleBusiness(models.Model):
    sme = models.ForeignKey(SME, on_delete=models.CASCADE)
    size_of_employees = models.ForeignKey(SizeValue, related_name='employee_sizes', on_delete=models.CASCADE)
    size_of_annual_revenue = models.ForeignKey(SizeValue, related_name='revenue_sizes', on_delete=models.CASCADE)
    size_of_asset_value = models.ForeignKey(SizeValue, related_name='asset_sizes', on_delete=models.CASCADE)
    rating = models.IntegerField()
    business_size = models.CharField(max_length=20)

    def __str__(self):
        return f"Business size: {self.business_size}, Rating: {self.rating}"