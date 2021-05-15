from django.shortcuts import render, redirect
from .models import Item
from products.models import Product
from django.db.models import Q


# Create your views here.
def cart_confirm(request):
    if request.user.is_authenticated:
        global items
        items = []
        item = request.GET.get('item', None)
        products = Product.objects.filter(name=item)
        for product in products:
            items.append(product)
        return render(request, "cart_confirm.html", {'products': products})
    else:
        return render(request, 'login.html')


def cart(request):
    if request.method == 'POST':
        global items
        quantity = request.POST.get('quantity', None)
        total_price = items[0].price * int(quantity)
        Item.objects.create(user=request.user, name=items[0].name,
                            quantity=int(quantity),
                            price=total_price, img_url=items[0].img_upload.url)
        pr = 0
        cart_item = Item.objects.filter(user=request.user)
        for i in cart_item:
                pr += i.price
        tax = pr * 0.12
        tax = round(tax, 2)
        total = pr + tax
        total = round(total, 2)
        return render(request, 'cart.html', {'products': cart_item, 'total': pr, 'tax': tax, 'amount': total, 'nbar': 'cart'})
    else:
        if request.user.is_authenticated:
            k = 0
            pr = 0
            cart_item = Item.objects.filter(user=request.user, status="In cart")
            for i in cart_item:
                k += 1
                pr += i.price
            tax = pr * 0.12
            tax = round(tax, 2)
            total = pr + tax
            total = round(total, 2)
            return render(request, 'cart.html', {'products': cart_item, 't': k, 'total': pr, 'tax': tax, 'amount': total, 'nbar': 'cart'})
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
            orders = Item.objects.filter(user=request.user, status="In cart")
            orders.update(status="Order received")
        
        t = 0
        amount_received = 0
        amount_out = 0
        orders = Item.objects.filter(Q(user=request.user) & (Q(status="Order received") | Q(status="Out for delivery") | Q(status="Delivered")))
        received_orders = Item.objects.filter(user=request.user, status="Order received")
        out_orders = Item.objects.filter(user=request.user, status="Out for delivery")
        not_delivered_orders = Item.objects.filter(Q(user=request.user) & (Q(status="Order received") | 
        Q(status="Out for delivery")))
        for i in not_delivered_orders:
            t += 1
        for j in received_orders:
            amount_received += j.price * 1.12
        for k in out_orders:
            amount_out += k.price * 1.12
        
        amount_received = round(amount_received, 2)
        amount_out = round(amount_out, 2)
        return render(request, 'orders.html', {'products': orders, 't': t, 'nbar': 'orders', 'received': amount_received, 
        'out': amount_out})
    else:
        return redirect('login')
