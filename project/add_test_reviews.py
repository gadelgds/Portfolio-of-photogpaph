"""
Скрипт для добавления тестовых отзывов
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from game.models import Review

# Удалим старые тестовые отзывы
Review.objects.all().delete()

# Создадим тестовые отзывы
test_reviews = [
    {
        'author_name': 'Мария Иванова',
        'email': 'maria@example.com',
        'rating': 5,
        'text': 'Отличный фотограф! Очень профессионально провел съемку нашей свадьбы. Фотографии получились просто волшебные. Рекомендую всем!',
        'is_approved': True
    },
    {
        'author_name': 'Алексей Петров',
        'rating': 5,
        'text': 'Делал портретную фотосессию. Результат превзошел все ожидания! Очень комфортная атмосфера во время съемки.',
        'is_approved': True
    },
    {
        'author_name': 'Екатерина С.',
        'email': 'kate@example.com',
        'rating': 4,
        'text': 'Хорошая работа, качественные фотографии. Единственное - немного долго ждала обработку, но результат того стоил.',
        'is_approved': True
    },
    {
        'author_name': 'Дмитрий',
        'rating': 5,
        'text': 'Профессионал своего дела! Фотосессия для семейного альбома прошла на ура. Дети были в восторге!',
        'is_approved': True
    },
    {
        'author_name': 'Анна Смирнова',
        'email': 'anna@example.com',
        'rating': 5,
        'text': 'Спасибо за прекрасные фотографии! Очень довольна результатом. Обязательно обращусь еще.',
        'is_approved': True
    }
]

for review_data in test_reviews:
    review = Review.objects.create(**review_data)
    print(f"✓ Создан отзыв от {review.author_name} - {review.rating}★")

print(f"\n✅ Создано {Review.objects.count()} тестовых отзывов")
print("Теперь открой http://localhost:8000/reviews/ чтобы увидеть их!")
