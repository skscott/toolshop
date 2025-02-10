from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceBulkCreateView, InvoicesViewSet

router = DefaultRouter()
router.register(r'invoices', InvoicesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bulk-create/', InvoiceBulkCreateView.as_view(), name='bulk-create'),

]