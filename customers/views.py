from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from invoices.models import Invoice
from .models import Customer
from .serializers import CustomersSerializer, CustomerBulkCreateSerializer
from invoices.serializers import InvoiceSerializer

class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomersSerializer

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

class CustomerWithInvoicesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.prefetch_related('invoices').all().order_by('id')
    serializer_class = CustomersSerializer


class CustomerBulkCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerBulkCreateSerializer

    def create(self, request, *args, **kwargs):
        # Ensure the serializer handles a list of objects
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)