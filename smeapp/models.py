from django.db import models

class SME(models.Model):
    company_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=500, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    number_of_employees = models.IntegerField(null=True, blank=True)
    established_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.company_name
