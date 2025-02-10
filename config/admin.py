from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from customers.models import Customer
from inventory.models import Inventory
from invoices.models import Invoice
from jobs.models import Job

# Ensure we unregister before registering
if admin.site.is_registered(User):
    admin.site.unregister(User)

admin.site.register(User, UserAdmin)

admin.site.register(Customer)
admin.site.register(Inventory)
admin.site.register(Job)
admin.site.register(Invoice)

