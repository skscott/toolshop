from django.db import models
from customers.models import Customer
from inventory.models import Inventory  
from django.utils.translation import gettext_lazy as _

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices")  # Customer who made the purchase
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    date_issued = models.DateField(auto_now_add=True)  # Date the invoice was created
    due_date = models.DateField()  # Due date for payment
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total amount for the invoice
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Tax amount (if any)
    
    status_choices = [
        ('NEW',  _('New')),
        ('PAID',  _('Paid')),
        ('PENDING',  _('Pendimg')),
        ('CANCELLED',  _('Cancelled')),
        ('INPROGRESS',  _('In Progress')),
        ('COMPLETED',  _('Completed')),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')  # Invoice status
    created_at = models.DateTimeField(auto_now_add=True)  # Created timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Updated timestamp

    class Meta:
        verbose_name_plural = "Inventory"

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.customer.name}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Use self.pk if available, otherwise fetch the next available ID
            next_id = self.pk or (Invoice.objects.latest('id').id + 1 if Invoice.objects.exists() else 1)
            self.invoice_number = f"INV-{next_id:06d}"  # Format: INV-000001
        super().save(*args, **kwargs)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoice_items', on_delete=models.CASCADE)
    inventory_item = models.ForeignKey(Inventory, related_name='invoice_items', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)