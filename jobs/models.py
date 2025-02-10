from django.db import models

from config.serializers import User
from customers.models import Customer
from django.utils.translation import gettext_lazy as _

class Job(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Customer requesting the service
    job_title = models.CharField(max_length=255)  # Title or brief description of the job
    description = models.TextField()  # Detailed description of the job
    status_choices = [
        ('NEW', _('New')),
        ('IN_PROGRESS', _('In Progress')),
        ('COMPLETED', _('Completed')),
        ('CANCELLED', _('Cancelled')),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='NEW')  # Current job status
    start_date = models.DateField()  # Start date of the job
    end_date = models.DateField(null=True, blank=True)  # Expected or actual completion date
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2)  # Estimated cost for the job
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Actual cost (if completed)
    created_at = models.DateTimeField(auto_now_add=True)  # Created timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Updated timestamp
    
    class Meta:
        verbose_name_plural = "Jobs" 

    def __str__(self):
        return f"Job: {self.job_title} for {self.customer}"