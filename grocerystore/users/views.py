from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Customer, Vendor
from django.contrib.auth.decorators import login_required
from .decorators import delivery_agent_required

# View for customer registration handling form submission and user creation
def customer_register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            address = request.POST['address']
            phone = request.POST['phone']

            if User.objects.filter(username=username).exists():
                return render(request, 'users/customer_register.html', 
                           {'error': 'Username already exists'})

            user = User.objects.create_user(username=username, password=password, email=email)
            Customer.objects.create(user=user, address=address, phone=phone)
            from django.contrib import messages
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        except Exception as e:
            return render(request, 'users/customer_register.html',
                       {'error': str(e)})
    return render(request, 'users/customer_register.html')

# View for vendor registration handling form submission and user creation
def vendor_register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            store_name = request.POST['store_name']
            phone = request.POST['phone']
            email = request.POST['email']

            if User.objects.filter(username=username).exists():
                return render(request, 'users/vendor_register.html', 
                           {'error': 'Username already exists'})

            user = User.objects.create_user(username=username, password=password, email=email)
            Vendor.objects.create(user=user, store_name=store_name, phone=phone)
            from django.contrib import messages
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        except Exception as e:
            return render(request, 'users/vendor_register.html',
                       {'error': str(e)})
    return render(request, 'users/vendor_register.html')

# View for delivery agent registration handling form submission and user creation
def delivery_register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            phone = request.POST['phone']
            region = request.POST['region']

            if User.objects.filter(username=username).exists():
                return render(request, 'users/delivery_register.html', 
                              {'error': 'Username already exists'})

            user = User.objects.create_user(username=username, password=password)
            from .models import DeliveryAgent
            DeliveryAgent.objects.create(user=user, phone=phone, region=region)
            from django.contrib import messages
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        except Exception as e:
            return render(request, 'users/delivery_register.html',
                          {'error': str(e)})
    return render(request, 'users/delivery_register.html')

from django.contrib.auth import authenticate, login, logout

# View for user login handling authentication and redirecting to appropriate dashboard
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
            elif hasattr(user, 'deliveryagent'):
                return redirect('delivery_dashboard')
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

# View for user logout and redirect to login page
def user_logout(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required
from users.decorators import customer_required, vendor_required

# Dashboard view for logged-in customers
@login_required
@customer_required
def customer_dashboard(request):
    return render(request, 'users/customer_dashboard.html')

# Dashboard view for logged-in vendors
@login_required
@vendor_required
def vendor_dashboard(request):
    return render(request, 'users/vendor_dashboard.html')

from .decorators import delivery_agent_required
from django.contrib.auth.decorators import login_required

# Dashboard view for logged-in delivery agents
@login_required
@delivery_agent_required
def delivery_dashboard(request):
    return render(request, 'users/delivery_dashboard.html')

# View to choose registration type
def choose_registration(request):
    return render(request, 'users/choose_registration.html')






