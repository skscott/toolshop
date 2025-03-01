from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from invoices.models import Invoice
from .models import Customer
from .serializers import CustomersInvoicesSerializer, CustomersJobsSerializer, CustomersSerializer, CustomerBulkCreateSerializer
from invoices.serializers import InvoiceSerializer
from logging import getLogger
from utils.etlogger import log_function_call

logger = getLogger('django')

class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomersSerializer

    @log_function_call
    def list(self, request, *args, **kwargs):
        ret = super(CustomersViewSet, self).list(request)
        return Response(sorted(ret.data, key=lambda k: k['name']))

    @log_function_call
    def create(self, request, *args, **kwargs):
        return super(CustomersViewSet, self).create(request)
    
    @log_function_call
    def retrieve(self, request, *args, **kwargs):
        return super(CustomersViewSet, self).retrieve(request)
    
    @log_function_call
    def update(self, request, *args, **kwargs):
        return super(CustomersViewSet, self).update(request)

class CustomersInvoicesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.prefetch_related('invoices').all().order_by('id')
    serializer_class = CustomersSerializer

class CustomerJobsView(generics.ListAPIView):
    serializer_class = CustomersJobsSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Customer.objects.filter(id=customer_id).prefetch_related('jobs').all().order_by('id')

class CustomerInvoicesView(generics.ListAPIView):
    serializer_class = CustomersInvoicesSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Customer.objects.filter(id=customer_id).prefetch_related('invoices').all().order_by('id')

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