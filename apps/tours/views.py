from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def services(request): return HttpResponse("Services")
def destinations(request): return HttpResponse("Destinations")
def packages(request): return HttpResponse("Packages")
def gallery(request): return HttpResponse("Gallery")