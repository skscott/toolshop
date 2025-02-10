from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inventory.views import InventoryViewSet
from invoices.views import InvoicesViewSet
from jobs.views import JobsViewSet
from .views import CustomObtainAuthToken, UserViewSet
from customers.views import CustomersViewSet, CustomerWithInvoicesViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('customers', CustomersViewSet)
router.register('customers-with-invoices', CustomerWithInvoicesViewSet, basename='customer-invoices')
router.register('inventory', InventoryViewSet)
router.register('invoices', InvoicesViewSet)
router.register('jobs', JobsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('admin/', admin.site.urls),
    
    path('api/authenticate/', CustomObtainAuthToken.as_view()),
    path("api-auth/", include("rest_framework.urls")),
    

    
    path('api/customers/', include('customers.urls')),  # Ensure this line is correct
    path('api/jobs/', include('jobs.urls')),
    path('api/invoices/', include('invoices.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/settings/', include('settings.urls')),
]