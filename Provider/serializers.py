
from rest_framework import serializers
from rest_framework.decorators import action
from Provider.models import User



class UserSerializer(serializers.ModelSerializer):
    """
    Class UserSerializer using serializers.ModelSerializers
    """
    class Meta:
        """
        class Meta to define fields for the model
        """
        model = User
        fields='__all__'
        # fields = ['username','email','first_name','last_name','phone_number','currency','language']
        # exclude=['password']
    
    def create(self,validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        return user

    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.language = validated_data.get('language', instance.language)
        instance.save()
        return instance