from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'email', 'username', 'profile']
        # fields= '__all__'
        depth=1
        
class MyTOKS(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token=super().get_token(user)
        token['full_name']=user.profile.full_name
        token['username']=user.username
        token['email']=user.email
        if user.profile.profile_picture:
            token['profile_picture'] = user.profile.profile_picture.url
        else:
            token['profile_picture'] = None
        return token

class RegisterationSerializer(serializers.ModelSerializer):
    full_name=serializers.CharField(max_length=100, write_only=True)
    password=serializers.CharField(max_length=100, write_only=True, validators=[validate_password,])
    password2=serializers.CharField(max_length=100, write_only=True)
    class Meta:
        model=User
        fields=['full_name', 'password', 'password2', 'email', 'username']
    
    def validate(self, attrs):
        if attrs['password']!=attrs['password2']:
            raise serializers.ValidationError({'password':'Passwords do not match '})
        return attrs
        
    def create(self, validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        user.profile.full_name=validated_data['full_name']
        user.profile.save()
        return user
  
        