from django.shortcuts import render
from .models import Product

products = Product.objects.all()


# Create your views here.
def index(request):
    return render(request, 'index.html', {'products': products})
