from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model
from django.http import HttpResponsePermanentRedirect

from utils.etlogger import log_function_call

from .serializers import UIComponentSimpleSerializer, UserSerializer, UIComponentSerializer
from .models import UIComponent

from rest_framework import viewsets
from .models import UIComponent
from .serializers import UIComponentSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [AllowAny]  # Open to everyone

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
        
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @log_function_call
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class UIComponentViewSet(viewsets.ModelViewSet):
    queryset = UIComponent.objects.all()
    serializer_class = UIComponentSimpleSerializer

    def get_queryset(self):
        queryset = UIComponent.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)