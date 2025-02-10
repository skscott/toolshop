from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobsViewSet

router = DefaultRouter()
router.register(r'jobs', JobsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

