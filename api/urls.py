from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .views import BundleViewSet

router = routers.DefaultRouter()
router.register(r'bundles', BundleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
