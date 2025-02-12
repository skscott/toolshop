from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets

from django.contrib.auth import get_user_model
from django.http import HttpResponsePermanentRedirect

from .serializers import UserSerializer, UIComponentSerializer
from .models import UIComponent

from rest_framework import viewsets
from .models import UIComponent
from .serializers import UIComponentSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def index(request):
    """Renders the home page."""
    if request.user.is_authenticated:
        return HttpResponsePermanentRedirect("/api/")

    return HttpResponsePermanentRedirect("/api-auth/login")

User = get_user_model()  # Ensure we always reference the correct User model

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        try:
            token = Token.objects.get(key=response.data['token'])
            user = User.objects.get(pk=token.user.pk)  # Ensure it's an actual User object
            user_data = UserSerializer(user).data
            return Response({'token': token.key, 'user': user_data})
        except Token.DoesNotExist:
            return Response({'error': 'Token does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        

class UIComponentViewSet(viewsets.ModelViewSet):
    queryset = UIComponent.objects.all()
    serializer_class = UIComponentSerializer
