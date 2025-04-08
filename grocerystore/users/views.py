from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Customer, Vendor

def customer_register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            address = request.POST['address']
            phone = request.POST['phone']

            if User.objects.filter(username=username).exists():
                return render(request, 'users/customer_register.html', 
                           {'error': 'Username already exists'})

            user = User.objects.create_user(username=username, password=password)
            Customer.objects.create(user=user, address=address, phone=phone)
            from django.contrib import messages
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        except Exception as e:
            return render(request, 'users/customer_register.html',
                       {'error': str(e)})
    return render(request, 'users/customer_register.html')

def vendor_register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            store_name = request.POST['store_name']
            phone = request.POST['phone']

            if User.objects.filter(username=username).exists():
                return render(request, 'users/vendor_register.html', 
                           {'error': 'Username already exists'})

            user = User.objects.create_user(username=username, password=password)
            Vendor.objects.create(user=user, store_name=store_name, phone=phone)
            from django.contrib import messages
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        except Exception as e:
            return render(request, 'users/vendor_register.html',
                       {'error': str(e)})
    return render(request, 'users/vendor_register.html')

from django.contrib.auth import authenticate, login, logout

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if hasattr(user, 'customer'):
                return redirect('customer_dashboard')
            elif hasattr(user, 'vendor'):
                return redirect('vendor_dashboard')
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required
from users.decorators import customer_required, vendor_required

@login_required
@customer_required
def customer_dashboard(request):
    return render(request, 'users/customer_dashboard.html')

@login_required
@vendor_required
def vendor_dashboard(request):
    return render(request, 'users/vendor_dashboard.html')



