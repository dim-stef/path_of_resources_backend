from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from bundle.models import Bundle, Paper
import stripe


class PaperSerializer(serializers.Serializer):
    url = serializers.CharField()
    nickname = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        fields = ['url', 'nickname', 'description']


class BundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bundle
        fields = ['name', 'description', 'image', 'price', 'price_id']
        read_only_fields = ['id']
