from django.shortcuts import render
from myapp.models import news, userTempData, userData, ris
from django.template import RequestContext
from rest_framework import viewsets
from myapp.serializers import newsSerializer, userTempDataSerializer, userDataSerializer, risSerializer
import requests
import json

class newsViewSet(viewsets.ModelViewSet):
    queryset = news.objects.all()
    serializer_class = newsSerializer

class userDataViewSet(viewsets.ModelViewSet):
    queryset = userData.objects.all()
    serializer_class = userDataSerializer

class userTempDataViewSet(viewsets.ModelViewSet):
    queryset = userTempData.objects.all()
    serializer_class = userTempDataSerializer

class risViewSet(viewsets.ModelViewSet):
    queryset = ris.objects.all()
    serializer_class = risSerializer

# Create your views here.
def home2(request):
    return render(request, 'myapp/index2.html', {})
def home(request):
    return render(request, 'myapp/index.html', {})
def home3(request):
    return render(request, 'myapp/index3.html', {})
def announcements(request):
    return render(request, 'myapp/announcements.html', {})