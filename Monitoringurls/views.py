from django.shortcuts import render
from rest_framework.decorators import api_view, APIView ,permission_classes, authentication_classes
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import authentication, permissions
from rest_framework.authentication import TokenAuthentication

from .models import urlslist, urlshistory, deletedurls
from .serializers import urlslistSerializer, urlshistorySerializer, deletedurlsSerializer
import requests
import datetime
 
# for timezone()
import pytz
from Monitoringurls.pagination import StandardResultsSetPagination

# Create your views here. 

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_urls(request):
    if request.method == 'GET':
        user = request.user
        Urlslist = urlslist.objects.filter(user_id=user)
        serializer = urlslistSerializer(Urlslist, many=True)
        for x in Urlslist:
            print(requests.get(x).status_code)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'DELETE':
        data = request.data
        user = request.user     
        
        url = urlslist.objects.get(url_name=data['url_name'], user_id=user)
        
        context = {
            "url_name":data['url_name'],
            "user_id": user.id,
            "created_at": str(datetime.datetime.now())
        }

        serializer = deletedurlsSerializer(data = context)

        if serializer.is_valid():
            serializer.save()

        url.delete()
        Urlslist = urlslist.objects.filter(user_id=user)
        serializer = urlslistSerializer(Urlslist, many=True)
        return JsonResponse("deleted", safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_deleted_urls(request):
    if request.method == 'GET':
        user = request.user

        urls = deletedurls.objects.filter(user_id=user)
        serializer = deletedurlsSerializer(urls, many=True)

        return JsonResponse(serializer.data, safe=False)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_urls_history(request):
    if request.method == 'POST':
        paginator = StandardResultsSetPagination()
        user = request.user
        data = request.data

        Urlshistory = urlshistory.objects.filter(urlslist__url_name=data['url_name'],)

        result_page = paginator.paginate_queryset(Urlshistory, request)
        #Urlshistory = urlshistory.objects.filter(urlslist__user_id= user, urlslist__url_name=data['url_name'])
        serializer = urlshistorySerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)




class urlCreateView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = urlslistSerializer
    def get(self, request, *args, **kwargs):
        urls = urlslist.objects.all()

        serializer = self.serializer_class(instance=urls, many=True)

        return Response(data=serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        data = request.data

        user = request.user
        
        try:
            response = requests.get(data["url_name"]).status_code

            if (response >=200 and response <= 226):
                status="ACTIVE"
            else:
                status="DOWN"    
        except:
            return  Response(data={"message":"website not available"})
               

        context={
            "url_name":data["url_name"],
            "status": status,
            "user_id": user.id

        }
        serializer = self.serializer_class(data=context)

        if serializer.is_valid():

            if not urlslist.objects.filter(user_id =user.id, url_name=data["url_name"]).exists():
                print("saved")
                serializer.save()
            else:
                print("not saved")
            
        return Response(data=serializer.data, status=201)    


class urlCreateHistory(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = urlshistorySerializer
    def get(self, request, *args, **kwargs):
        urls = urlshistory.objects.all()

        serializer = self.serializer_class(instance=urls, many=True)

        return Response(data=serializer.data, status=200)

    def post(self, request, *args, **kwargs):

        user = request.user

        urls = urlslist.objects.all()

        for url in urls:

            response = requests.get(str(url)).status_code
        
            if (response == 200):
                status="ACTIVE"
            else:
                status="DOWN"

            current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

            context={
            "created_at":str(current_time),
            "updated_at":str(current_time),
            "status": status,
            "urlslist": url.id
            }

            serializer = self.serializer_class(data=context)

            if serializer.is_valid():
                serializer.save()
               

        context={
            "created_at":current_time,
            "updated_at":current_time,
            "status": status,
            "urlslist": ""

        }

            
        return Response(data=serializer.data, status=201)    