from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerJobsView, CustomersViewSet, CustomerInvoicesView, CustomerBulkCreateView

router = DefaultRouter()
router.register(r'customers', CustomersViewSet, basename='customers')

urlpatterns = [
    path('customers/<int:customer_id>/invoices/', CustomerInvoicesView.as_view(), name='customer-invoices'),
    path('customers/<int:customer_id>/jobs/', CustomerJobsView.as_view(), name='customer-jobs'),
    path('customers/bulk-create/', CustomerBulkCreateView.as_view(), name='bulk-create'),
    path('', include(router.urls)),  # Ensures /api/customers/ structure
]   
