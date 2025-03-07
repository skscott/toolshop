from rest_framework import serializers
from .models import Job
from customers.models import Customer

class JobsSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Job
        fields = '__all__'

