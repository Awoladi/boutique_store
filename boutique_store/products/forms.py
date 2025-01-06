# products/forms.py
from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a Category"
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'image']
