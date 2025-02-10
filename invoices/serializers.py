from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceBulkSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        invoices = [Invoice(**item) for item in validated_data]
        return Invoice.objects.bulk_create(invoices)

class InvoiceBulkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        list_serializer_class = InvoiceBulkSerializer