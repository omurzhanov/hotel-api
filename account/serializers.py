from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import send_activation_code
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from rooms.models import *
from rest_framework.settings import api_settings

'''REGISTER'''


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirmation = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'password_confirmation', 'superhost']

    def validate_email(self, email):
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User already exists')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Passwords do not match')
        return attrs
    def validate_superhost(self, superhost):
        return superhost

    def create(self, validated_data):
        print(validated_data)
        email = validated_data.get('email')
        password = validated_data.get('password')
        superhost = validated_data.get('superhost')
        user = MyUser.objects.create_user(email=email, password=password, superhost=superhost)
        send_activation_code(email=email, activation_code=user.activation_code)
        return user

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label=('password'),
        style={'input_type':'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs