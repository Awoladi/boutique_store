from django.urls import path, include
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('products/', include('products.urls', namespace='products')),
]
