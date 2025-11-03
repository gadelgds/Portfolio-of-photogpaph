from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('services/', views.services, name='services'),
]