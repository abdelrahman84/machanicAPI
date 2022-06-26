from rest_framework import serializers

from cars.models import Car


class CarSerializer (serializers.Serializer):

    name = serializers.CharField(required=True)
    model = serializers.CharField(required=True)
    manufacturing_date = serializers.IntegerField(required=True)
    total_distance = serializers.DecimalField(required=True,max_digits=64,decimal_places=2)

    def create(self, validated_data):
      return Car(**validated_data) 