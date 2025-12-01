from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),
    path('services/', views.services, name='services'),
    path('reviews/', views.reviews, name='reviews'),
    path('contact/', views.contact, name='contact'),
    path('order/<int:service_id>/', views.create_order, name='create_order'),
    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]