from django.shortcuts import render
from products.models import Product
import random
from datetime import datetime

items = Product.objects.all()
products = []

for item in items:
    products.append(item)

# Create your views here.
def home(request):
    random.seed(datetime.now())
    random.shuffle(products)
    return render(request, 'home.html', {'products': products, 'nbar': 'home'})


def contact(request):
    return render(request, 'contact.html', {'nbar': 'contact'})


def about(request):
    return render(request, 'about.html')
