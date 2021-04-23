from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, CustomLoginSerializer, CreateNewPasswordSerializer
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import MyUser
from .utils import send_activation_email
from rest_framework.permissions import AllowAny

class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully registered', status = status.HTTP_200_OK)
        return Response('Not valid info', status=status.HTTP_400_BAD_REQUEST)

class ActivationView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(MyUser, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response("Your account is successfully activated", status=status.HTTP_200_OK)

class LoginView(ObtainAuthToken):
    serializer_class = CustomLoginSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)

class ForgotPassword(APIView):
    permission_classes = [AllowAny,]
    def get(self, request):
        User = get_user_model()
        email = request.query_params.get('email')
        user = get_object_or_404(User, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_email(email=email, activation_code=user.activation_code)
        return Response('Activation code has been sent to your email', status=status.HTTP_200_OK)

class ForgotPasswordComplete(APIView):
    def post(self, request):
        data = request.data
        serializer = CreateNewPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('You have successfully reset your password', status=status.HTTP_200_OK)

