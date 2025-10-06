from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Feature
from .serializers import FeatureSerializer


class FeatureViewSet(viewsets.ViewSet):
    """
    Feature ViewSet with only GET operations
    """

    @classmethod
    def list(cls, request):
        features = Feature.objects.all()
        serializer = FeatureSerializer(features, many=True)
        return Response(serializer.data)

    @classmethod
    def retrieve(cls, request, pk=None):
        feature = get_object_or_404(Feature, pk=pk)
        serializer = FeatureSerializer(feature)
        return Response(serializer.data)
