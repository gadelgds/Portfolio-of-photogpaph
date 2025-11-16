from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),  # Маршрут для лайков
    path('services/', views.services, name='services'),
    path('reviews/', views.reviews, name='reviews'),  # Новый маршрут для отзывов
    path('contact/', views.contact, name='contact'),  # Маршрут для контактов
]