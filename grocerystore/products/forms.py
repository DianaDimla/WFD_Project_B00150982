from django import forms
from .models import Product

# Form class for creating and updating Product instances
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock', 'is_available', 'image']
        widgets = {
            'is_available': forms.HiddenInput(),
        }
