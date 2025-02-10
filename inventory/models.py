from django.db import models

class Inventory(models.Model):
    name = models.CharField(max_length=255)  # Product Name
    description = models.TextField()  # Product Description
    quantity_in_stock = models.IntegerField(default=0)  # Available Quantity
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Unit Price
    category = models.CharField(max_length=100, blank=True, null=True)  # Product Category (optional)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Stock Keeping Unit (optional)
    created_at = models.DateTimeField(auto_now_add=True)  # When it was added
    updated_at = models.DateTimeField(auto_now=True)  # When it was last updated
    
    class Meta:
        verbose_name_plural = "Inventory"

    def __str__(self):
        return self.name