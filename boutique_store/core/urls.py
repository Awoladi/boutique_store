from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home_page'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]