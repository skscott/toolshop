from rest_framework import serializers
from .models import SalesOrder, SalesOrderLine

class SalesOrderLineSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = SalesOrderLine
        fields = ['id', 'sales_order', 'product', 'product_name', 'quantity', 'price_per_unit', 'total_price']
        read_only_fields = ['total_price']

class SalesOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    order_lines = SalesOrderLineSerializer(many=True, read_only=True)

    class Meta:
        model = SalesOrder
        fields = ['id', 'sales_order_number', 'customer', 'customer_name', 'order_date', 'status', 'order_lines']
