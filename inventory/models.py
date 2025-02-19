from django.db import models

class Inventory(models.Model):
    name = models.CharField(max_length=255)  # Warehouse or Category
    description = models.TextField(blank=True)  # Optional Description
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Inventory"

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="items")  # Inventory Link
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True)  # Stock Keeping Unit
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} (SKU: {self.sku})"
