from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from bundle.models import Bundle, BundleType, Paper
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
        fields = ['name', 'slug', 'description', 'image', 'price', 'price_id']
        read_only_fields = ['id']


class BundleTypeSerializer(serializers.ModelSerializer):
    number_of_bundles = serializers.SerializerMethodField()

    def get_number_of_bundles(self, bundle_type):
        return bundle_type.bundles.count()

    class Meta:
        model = BundleType
        fields = ['name', 'slug', 'image', 'number_of_bundles']