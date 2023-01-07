from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from .models import User
from django.contrib.auth.hashers import make_password
#from django.contrib.auth.models import User




class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()   

    def validate(self, data):

        if data['email']:
            if User.objects.filter(email= data['email']).exists():
                raise serializers.ValidationError('email is taken')

        return data

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'], password = make_password(validated_data['password']))
        
        #user.make_password(validated_data['password'])
        #print(user["password"])
        print(validated_data['password'])  
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()         






















"""
class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username=serializers.CharField(max_length=50)
    password=serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationError("Email has already been used")

        return super().validate(attrs)   
    

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'], username=validated_data['username'], password = validated_data['password'])
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()  

    class Meta:
        model = User
        fields = ['email', 'password']"""