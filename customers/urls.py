from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomersViewSet, CustomerBulkCreateView

router = DefaultRouter()
router.register(r'customers', CustomersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bulk-create/', CustomerBulkCreateView.as_view(), name='bulk-create'),
]