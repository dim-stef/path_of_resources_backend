from rest_framework import routers, serializers, viewsets
from bundle.models import Bundle, Paper
from .serializers import BundleSerializer

class BundleViewSet(viewsets.ModelViewSet):
    queryset = Bundle.objects.all()
    serializer_class = BundleSerializer

    # def create(self, request):
    #     serializer = self.serializer_class()
    #     data = serializer.data
    #     return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
