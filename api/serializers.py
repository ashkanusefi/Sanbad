from rest_framework import serializers
from api.models import CityClimate


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityClimate
        fields = ['temp']
