from django.db import models
from customers.models import Customer  # Import from the customer app
from inventory.models import InventoryItem   # Import from inventory app

class SalesOrder(models.Model):
    sales_order_number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales_orders')
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('NEW', 'New'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.sales_order_number:
            last_order = SalesOrder.objects.order_by('-id').first()
            last_number = int(last_order.sales_order_number.split('-')[-1]) if last_order else 0
            self.sales_order_number = f"SO-{last_number + 1:06d}"  # Format: SO-000001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sales Order {self.sales_order_number} - {self.customer.name}"

class SalesOrderLine(models.Model):
    sales_order = models.ForeignKey("SalesOrder", on_delete=models.CASCADE, related_name="order_lines")
    product = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="sales_order_lines")
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.sales_order.sales_order_number}"

