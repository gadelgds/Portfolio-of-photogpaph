from django.shortcuts import render, get_object_or_404
from .models import Photo, Service

def home(request):
    photos = Photo.objects.all()
    return render(request, 'game/home.html', {'photos': photos})  # Изменили portfolio на game

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'game/photo_detail.html', {'photo': photo})  # Изменили portfolio на game

def services(request):
    services = Service.objects.all()
    return render(request, 'game/services.html', {'services': services})  # Изменили portfolio на game