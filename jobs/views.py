from rest_framework import viewsets
from .models import Job
from .serializers import JobsSerializer

class JobsViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobsSerializer

