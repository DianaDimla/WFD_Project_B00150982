from django.urls import path
from . import views

urlpatterns = [
    path('browse/', views.browse_products, name='browse_products'),
]
