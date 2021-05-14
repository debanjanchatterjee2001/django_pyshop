from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1,
                                                first_name=first_name, last_name=last_name)
                user.save()
                customer = auth.authenticate(username=username, password=password1)
                auth.login(request, customer)
                return redirect('/')

        else:
            messages.info(request, "Password didn't match")
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        customer = auth.authenticate(username=username, password=password)

        if customer is not None:
            auth.login(request, customer)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
