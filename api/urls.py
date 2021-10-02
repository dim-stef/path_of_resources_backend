from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .views import BundleViewSet, webhook, create_checkout_session

router = routers.DefaultRouter()
router.register(r'bundles', BundleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/webhooks/stripe/', webhook, name="stripe_webhook"),
    path('v1/create_checkout_session/', create_checkout_session, name="create-checkout-session"),
]

#create-checkout-session