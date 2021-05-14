from django.shortcuts import render, redirect
from .models import Item
from products.models import Product
from django.db.models import Q


# Create your views here.
def cart_confirm(request):
    if request.user.is_authenticated:
        global items
        item = request.GET.get('item', None)
        products = Product.objects.filter(name=item)
        items = []
        for product in products:
            items.append(product)
        return render(request, "cart_confirm.html", {'products': products})
    else:
        return render(request, 'login.html')


def cart(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', None)
        total_price = items[0].price * int(quantity)
        Item.objects.create(user=request.user, name=items[0].name,
                            quantity=int(quantity),
                            price=total_price, img_url=items[0].img_upload.url)
        cart_item = Item.objects.filter(user=request.user)
        return render(request, 'cart.html', {'products': cart_item})
    else:
        if request.user.is_authenticated:
            t = 0
            cart_item = Item.objects.filter(user=request.user)
            for i in cart_item:
                t += 1
            return render(request, 'cart.html', {'products': cart_item, 't': t})
        else:
            return redirect('login')


def delete_item(request):
    user = request.user
    item = request.GET.get('item', None)
    cart_item = Item.objects.filter(user=user, name=item)
    cart_item.delete()
    return render(request, 'delete_item.html')


def orders(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            orders = Item.objects.filter(status="In cart")
            orders.update(status="Order received")
        orders = Item.objects.filter(Q(status="Order received") | Q(status="Out for delivery") | Q(status="Delivered"))
        return render(request, 'orders.html', {'products': orders})
    else:
        return redirect('login')
