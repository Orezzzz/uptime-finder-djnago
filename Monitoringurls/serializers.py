from rest_framework import serializers
from .models import urlslist, urlshistory, deletedurls
  
class urlslistSerializer(serializers.ModelSerializer):
    class Meta:
        model = urlslist
        fields = "__all__"


class urlshistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = urlshistory
        fields = "__all__"        


class deletedurlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = deletedurls
        fields = "__all__"        