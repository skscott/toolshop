from django.db import models
from django_countries.fields import CountryField  # For country selection
from phonenumber_field.modelfields import PhoneNumberField  # For international phone numbers

class Customer(models.Model):
    COMPANY_TYPES = [
        ('sole_trader', 'Sole Trader'),
        ('partnership', 'Partnership'),
        ('limited', 'Limited Liability Company (Ltd)'),
        ('public', 'Public Limited Company (PLC)'),
        ('cooperative', 'Cooperative'),
        ('nonprofit', 'Non-Profit Organization'),
        ('technology', 'ICT Company'),
        ('creative', 'Arts and Farts'),
        ('environmental', 'Environment - Money down the drain'),
        ('media', 'Media - State propaganda'),
        ('design', 'Design - one for life'),
        ('finance', 'Dodgy deals in back rooms'),
        ('marketing', 'Marketing'),
        ('healthcare', 'Healthcare'),
        ('construction', 'Construction'),
    ]

    name = models.CharField(max_length=255, unique=True, help_text="Registered business name")
    vat_number = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="EU VAT Number (if applicable)")
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPES, help_text="Legal structure of the business")
    
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = CountryField()  # Django-Countries package for country selection

    contact_name = models.CharField(max_length=100, help_text="Primary contact person")
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(region="NL", help_text="International format phone number")

    industry = models.CharField(max_length=100, blank=True, help_text="Industry sector (e.g., IT, Retail, Manufacturing)")
    website = models.URLField(blank=True, null=True, help_text="Company website")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True, help_text="Indicates if the customer is active")

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.country})"
