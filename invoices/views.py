from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer, InvoiceBulkCreateSerializer

class InvoicesViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

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