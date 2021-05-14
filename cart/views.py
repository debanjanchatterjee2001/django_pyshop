from django.shortcuts import render, redirect
from .models import Item
from products.models import Product


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
            cart_item = Item.objects.filter(user=request.user)
            return render(request, 'cart.html', {'products': cart_item})
        else:
            return redirect('login')


def delete_item(request):
    user = request.user
    item = request.GET.get('item', None)
    cart_item = Item.objects.filter(user=user, name=item)
    cart_item.delete()
    return render(request, 'delete_item.html')
