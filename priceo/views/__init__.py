from django.shortcuts import render
from priceo.models import Product

def home(request):
    return render(request, 'home.html')