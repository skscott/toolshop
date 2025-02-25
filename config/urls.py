from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inventory.views import InventoryViewSet
from invoices.views import InvoicesViewSet
from jobs.views import JobsViewSet
from .views import CustomObtainAuthToken, LogoutView, UIComponentViewSet, UserViewSet

router = DefaultRouter()
router.register('api/ui-components', UIComponentViewSet)

urlpatterns = [
    path("", include(router.urls)),  # Registers UI components, users, inventory, invoices, jobs
    path('admin/', admin.site.urls),

    path('api/authenticate/', CustomObtainAuthToken.as_view()),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
    path("api-auth/", include("rest_framework.urls")),

    # Ensure customers API is correctly structured
    path('api/', include('customers.urls')),  # Ensures /api/customers/ structure
    path('api/', include('invoices.urls')),   # Invoices API under /api/invoices/
    path('api/', include('jobs.urls')),
    path('api/', include('invoices.urls')),
    path('api/', include('inventory.urls')),
    path('api/', include('settings.urls')),
]
