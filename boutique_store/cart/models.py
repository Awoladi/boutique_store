from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.apps import apps

def get_product_model():
    return apps.get_model('products', 'Product')


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} (x{self.quantity})'

class Meta:
    unique_together = ('user', 'product')
