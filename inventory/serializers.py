from rest_framework import serializers
from .models import Inventory, InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    inventory_name = serializers.CharField(source='inventory.name', read_only=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'name', 'description', 'sku', 'price', 'stock_quantity', 'inventory', 'inventory_name']

class InventorySerializer(serializers.ModelSerializer):
    items = InventoryItemSerializer(many=True, read_only=True)  # Nested Items

    class Meta:
        model = Inventory
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'items']
