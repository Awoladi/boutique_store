from django.urls import path
from . import views
from .views import home_page

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home_page'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
