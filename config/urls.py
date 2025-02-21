from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inventory.views import InventoryViewSet
from invoices.views import InvoicesViewSet
from jobs.views import JobsViewSet
from .views import CustomObtainAuthToken, UIComponentViewSet, UserViewSet

router = DefaultRouter()
router.register('ui-components', UIComponentViewSet)
router.register('users', UserViewSet)
router.register('inventory', InventoryViewSet)
router.register('invoices', InvoicesViewSet)
router.register('jobs', JobsViewSet)

urlpatterns = [
    path("", include(router.urls)),  # Registers UI components, users, inventory, invoices, jobs
    path('admin/', admin.site.urls),

    path('api/authenticate/', CustomObtainAuthToken.as_view()),
    path("api-auth/", include("rest_framework.urls")),

    # Ensure customers API is correctly structured
    path('api/', include('customers.urls')),  # Ensures /api/customers/ structure
    path('api/', include('invoices.urls')),   # Invoices API under /api/invoices/
    path('api/jobs/', include('jobs.urls')),
    path('api/invoices/', include('invoices.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/settings/', include('settings.urls')),
]
