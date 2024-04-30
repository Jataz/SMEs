from django.db import models

class SME(models.Model):
    company = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    email = models.EmailField()
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=500)
    sector = models.CharField(max_length=100)
    type_of_business = models.CharField(max_length=100)
    product_service = models.CharField(max_length=500)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    number_of_employees = models.IntegerField()
    asset_value= models.DecimalField(max_digits=15, decimal_places=2)
    size_of_business = models.CharField(max_length=100)

    def __str__(self):
        return self.company
