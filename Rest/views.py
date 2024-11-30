from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Sum,Count
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import  check_password
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from Rest.helpscript import dates
import json
import os
project_root = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(project_root, 'dummy_list.json')

# this is a serializer used to handle valdiation and insertion for registartion#
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    #the password is not saved in the database for security reasons 
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

#this view works on a post method
#first it checks the data using the serializer
#on validation it inserts the data and repsonds with status 201 and a message to notify the user
#on faliure it responds with status 400 and a message to notify the user
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        try:
            data=request.data
            profile = Profile.objects.create(
                name=data.get('username'),
                type=data.get('type'),
                titles='nothing at the moment',
                description='add your description here',
                email=data.get('email'),
                image_url=''
            )
            profile.save()
        except Exception as e:
             return Response({'status': 'failure', 'errors': {'username': 'username already in use'},'message':  str(e)}, status=status.HTTP_400_BAD_REQUEST)  
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'success', 'user_id': user.id, 'message': 'Registration successful'}, status=status.HTTP_201_CREATED)

        return Response({'status': 'failure', 'errors': {'username': 'username already in use'},'message': 'username already in use'}, status=status.HTTP_400_BAD_REQUEST)

#this is the login view
##first it checks if the user is in the database
##if faliure it responds with status 400 and a message to notify the user about the wrong username
## on sucess it uses django middle ware for authenticaon o
## if sucess the user is sent a status 200 , a token and a message to notify the user 
## on faliure it responds with status 400 and a messsage to notify the user
class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow non-authenticated users to log in

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({ 'status': 'failure','message': 'wrong username','errors': {'username': 'Invalid username'} }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        profile = Profile.objects.get(name=request.data.get('username'))
        profile_data = {
            'profile_name': profile.name,
            'profile_type': profile.type,
            'profile_titles': profile.titles,
            'profile_description': profile.description,
            'profile_email': profile.email,
            'profile_image_url': profile.image_url,
        }
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'status': 'success',
                'message': 'Authentication successful',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'profile':profile_data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'failure',
            'message': 'Invalid username or password',
            'errors': {'username': 'Invalid username', 'password': 'Invalid password'}
        }, status=status.HTTP_400_BAD_REQUEST)

##this is the refresh token view
##this functions uses django middle ware to checks for the validty of the session
## on sucess it responds with a valid access token
## on faliure it notifies the user the session has ended and an error status
class RefreshAccessTokenView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        # Get refresh token from request data
        data = request.data
        refresh_token = data.get('refresh', None)

        if not refresh_token:
            return Response(
                {'status': 'failure', 'message': 'Session has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Decode and verify the refresh token using simplejwt
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return Response(
                {
                    'status': 'success',
                    'message': 'Welcome back',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e), 'status': 'failure', 'message': 'Session has expired', 'token': refresh_token},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )