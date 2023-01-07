from django.shortcuts import render
from django.contrib.auth import authenticate
from .serializers import  RegisterSerializer, LoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse, JsonResponse

#from django.contrib.auth import authenticate


 

# Create your views here.

class RegisterAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors
            })
        
        serializer.save()
        serializerlogin = LoginSerializer(data = data)

        if not serializerlogin.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors
            })

        user = authenticate(email = serializerlogin.data['email'], password = serializerlogin.data['password'])
        if not user:
            return Response({"user" : "not a user"})
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"username": str(user), "token": str(token)})




class LoginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        
        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors
            })

        user = authenticate(email = serializer.data['email'], password = serializer.data['password'])

        if not user:
            return Response({"user" : "not a user"})
        token, _ = Token.objects.get_or_create(user=user)
        print(user)
        
        return Response({"username": str(user), "token": str(token)})































