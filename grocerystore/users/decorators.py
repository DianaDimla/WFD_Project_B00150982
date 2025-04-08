from django.http import HttpResponseRedirect
from django.shortcuts import redirect

def customer_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if hasattr(request.user, 'customer'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # or an unauthorized page
    return wrapper_func

def vendor_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if hasattr(request.user, 'vendor'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # or an unauthorized page
    return wrapper_func
