"""
Скрипт для восстановления данных из папки media
Запускать: python manage.py shell < restore_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from game.models import Photo, Service

# Очистим старые данные (если есть)
Photo.objects.all().delete()
Service.objects.all().delete()

# Восстановим фотографии из папки media
photos_data = [
    {
        'title': 'Картинка в машине',
        'image': 'photos/1647529194_1-amiel-club-p-kartinki-v-mashine-2.jpg',
        'preview': 'previews/1647529194_1-amiel-club-p-kartinki-v-mashine-2.jpg'
    },
    {
        'title': 'Снимок экрана',
        'image': 'photos/Снимок_экрана_1.png',
        'preview': 'previews/Снимок_экрана_1.png'
    }
]

for photo_data in photos_data:
    photo = Photo.objects.create(**photo_data)
    print(f"✓ Создано фото: {photo.title}")

# Восстановим примеры услуг (замени на свои данные)
services_data = [
    {
        'name': 'Фотосессия портретная',
        'description': 'Профессиональная портретная фотосессия в студии или на природе',
        'price': 5000.00
    },
    {
        'name': 'Свадебная съемка',
        'description': 'Полный день съемки вашей свадьбы с обработкой фотографий',
        'price': 25000.00
    },
    {
        'name': 'Обработка фотографий',
        'description': 'Профессиональная ретушь и цветокоррекция ваших фотографий',
        'price': 500.00
    }
]

for service_data in services_data:
    service = Service.objects.create(**service_data)
    print(f"✓ Создана услуга: {service.name}")

print("\n✅ Данные успешно восстановлены!")
print(f"Всего фото: {Photo.objects.count()}")
print(f"Всего услуг: {Service.objects.count()}")
