from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.views import InventoryViewSet, InventoryItemViewSet

router = DefaultRouter()
router.register(r'inventory', InventoryViewSet)
router.register(r'inventory-items', InventoryItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
