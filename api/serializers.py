from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from bundle.models import Bundle, Paper


class PaperSerializer(serializers.Serializer):
    url = serializers.CharField()
    nickname = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        fields = ['url', 'nickname', 'description']


class BundleSerializer(serializers.ModelSerializer):
    papers = PaperSerializer(many=True)

    class Meta:
        model = Bundle
        fields = ['name', 'papers']
        read_only_fields = ['_id']
