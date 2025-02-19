from rest_framework import serializers

from invoices.serializers import InvoiceSerializer
from .models import Customer

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CustomersInvoicesSerializer(serializers.ModelSerializer):
    invoices = InvoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerBulkSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        customers = [Customer(**item) for item in validated_data]
        return Customer.objects.bulk_create(customers)

class CustomerBulkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        list_serializer_class = CustomerBulkSerializer