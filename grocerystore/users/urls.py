from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/customer/', views.customer_register, name='customer_register'),
    path('register/vendor/', views.vendor_register, name='vendor_register'),
    path('register/delivery/', views.delivery_register, name='delivery_register'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('delivery/dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path('register/', views.choose_registration, name='choose_registration'),
    

]
