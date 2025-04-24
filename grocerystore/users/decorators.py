from django.http import HttpResponseRedirect
from django.shortcuts import redirect

# Decorator to restrict access to customers only
def customer_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if hasattr(request.user, 'customer'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return wrapper_func

# Decorator to restrict access to vendors only
def vendor_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if hasattr(request.user, 'vendor'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  
    return wrapper_func

# Decorator to restrict access to delivery agents only
def delivery_agent_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if hasattr(request.user, 'deliveryagent'):
            return view_func(request, *args, **kwargs)
        return HttpResponse("Access Denied: Delivery Agents only.")
    return wrapper_func
