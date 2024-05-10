from django.shortcuts import render
from rest_framework.decorators import permission_classes,api_view,authentication_classes
from rest_framework.authentication import TokenAuthentication
from .serializers import UserInputSerializer,UserSerializer,UserLoginInputSerializer
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

@api_view(["POST"])
def sign_up(request):
    try:
        with transaction.atomic():
            user_serializer = UserInputSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                name = user_serializer.validated_data.get("username")
                password = user_serializer.validated_data.get("password")
                user = User.objects.get(username=name,password=password)
                if user:
                    token,success = Token.objects.get_or_create(user=user)
                    return Response({"message":"User Successfully created.","token":str(token)})
                return Response(status=status.HTTP_404_NOT_FOUND,data={"message":"User failed to create."})
            else:    
                return Response(status=status.HTTP_400_BAD_REQUEST,data=user_serializer.errors)
    except Exception as e:
        transaction.rollback()
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,data={"error":str(e)})

@api_view(["GET"])
def login(request):
    try:
        user_serializer = UserLoginInputSerializer(data=request.data)
        if user_serializer.is_valid():
            name = user_serializer.validated_data.get("username")
            password = user_serializer.validated_data.get("password")
            user = User.objects.get(username=name, password=password)
            if not user:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
            token,_ = Token.objects.get_or_create(user=user)
            return Response(status=status.HTTP_200_OK,data={"token":str(token),"user":UserSerializer(user).data})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=user_serializer.errors)
    except Exception as e:
        transaction.rollback()
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,data={"error":str(e)})