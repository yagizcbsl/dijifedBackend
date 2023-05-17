from rest_framework import serializers
from .models import ProfileTable, extraUserFields
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = extraUserFields
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileTable
        fields = "__all__"
        
class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileTable
        fields = ["profilePicture"]
        
class CoverPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileTable
        fields = ["coverPage"]