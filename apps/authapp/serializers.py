# authapp/serializers.py
from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()

class UserFormValidate:
    def validate_password(self, value):
        if len(value) < 8 or not set(value).intersection(set('0987654321')):
            raise serializers.ValidationError("8 letters or more, must contains numbers")
        return value

    def validate_password2(self, value):
        
        if value != self.initial_data.get('password'):
            raise serializers.ValidationError("Passwords do not match.")
        return value


class RegistrationSerializer(UserFormValidate, serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user  
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']