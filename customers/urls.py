from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomerInvoicesView, CustomersInvoicesViewSet, CustomersViewSet, CustomerBulkCreateView

router = DefaultRouter()
router.register('invoices', CustomersInvoicesViewSet, basename='customer-invoices')
router.register(r'customers', CustomersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:customer_id>/invoices/', CustomerInvoicesView.as_view(), name='customer-invoices'),
    path('bulk-create/', CustomerBulkCreateView.as_view(), name='bulk-create'),
]