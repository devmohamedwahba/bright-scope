from rest_framework import serializers
from .models import Feature

class FeatureSerializer(serializers.ModelSerializer):
    icon = serializers.CharField(default="fa-solid fa-star")
    class Meta:
        model = Feature
        fields = "__all__"
