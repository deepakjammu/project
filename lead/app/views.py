from django.shortcuts import render
from django.http import  HttpResponse
# Create your views here.
def home(request):

    return render(request,'home.html')

def index(request):

    return render(request,'index.html')

def call(request):

    return render(request, 'calling.html')  

def counselling(request):

    return render(request, 'counselling.html')      

def walkin(request):

    return render(request, 'walkin.html')          