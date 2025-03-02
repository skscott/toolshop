from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Invoice
from .serializers import InvoiceSerializer, InvoiceBulkCreateSerializer

from logging import getLogger
from utils.etlogger import log_function_call

logger = getLogger('django')
class InvoicesViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    @log_function_call
    def list(self, request, *args, **kwargs):
        ret = super(InvoicesViewSet, self).list(request)
        return Response(ret.data)
    
    @log_function_call
    def create(self, request, *args, **kwargs):
        return super(InvoicesViewSet, self).create(request)
    
    @log_function_call
    def retrieve(self, request, *args, **kwargs):
        return super(InvoicesViewSet, self).retrieve(request)
    
    @log_function_call
    def update(self, request, *args, **kwargs):
        return super(InvoicesViewSet, self).update(request)
    
    # Add a custom action to get the last invoice
    @action(detail=False, methods=['get'])
    def last_invoice(self, request):
        """
        Retrieve the last invoice record.
        """
        last_invoice = Invoice.objects.last()  # Get the last invoice by primary key
        if last_invoice:
            serializer = self.get_serializer(last_invoice)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No invoices found."}, status=status.HTTP_404_NOT_FOUND)
        
class InvoiceBulkCreateView(generics.CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceBulkCreateSerializer

    def create(self, request, *args, **kwargs):
        # Ensure the serializer handles a list of objects
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)