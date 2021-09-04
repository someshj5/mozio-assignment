
from rest_framework import serializers
from rest_framework.decorators import action
from geojson.models import Polygon,PolygonCoordinates

class RegionSerializer(serializers.ModelSerializer):
    """
    Class RegionSerializer using serializers.ModelSerializers
    """

    class Meta:
        """
        class Meta to define fields for the model
        """
        model = Polygon
        fields='__all__'
        depth=1
    
    def create(self, validated_data):
        return Polygon.objects.create(**validated_data)

    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.price = validated_data.get('price', instance.price)
        instance.provider = validated_data.get('provider', instance.provider)
        instance.save()
        return instance

class PolygonCoordinatesSerializer(serializers.ModelSerializer):
    # polygoin_id=RegionSerializer()

    class Meta:
        model=PolygonCoordinates
        fields='__all__'
        depth=1