from django.contrib.auth.models import User
from rest_framework import serializers

class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')
    
    def create(self, data):
        username = data.get("username",None)
        password = data.get("password",None)
        user = User.objects.create(username=username,password=password)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserLoginInputSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True)
    

