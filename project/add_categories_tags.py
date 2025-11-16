"""
Скрипт для добавления тестовых категорий и тегов
Запустите: python manage.py shell < add_categories_tags.py
"""

from game.models import Category, Tag

# Создаем категории
categories_data = [
    {'name': 'Портреты', 'slug': 'portraits'},
    {'name': 'Пейзажи', 'slug': 'landscapes'},
    {'name': 'Свадьбы', 'slug': 'weddings'},
    {'name': 'События', 'slug': 'events'},
    {'name': 'Студийная съемка', 'slug': 'studio'},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={'name': cat_data['name']}
    )
    if created:
        print(f"✓ Создана категория: {category.name}")
    else:
        print(f"- Категория уже существует: {category.name}")

# Создаем теги
tags_data = ['Природа', 'Люди', 'Черно-белое', 'Цветное', 'Закат', 'Город', 'Семья', 'Дети']

for tag_name in tags_data:
    tag, created = Tag.objects.get_or_create(name=tag_name)
    if created:
        print(f"✓ Создан тег: {tag.name}")
    else:
        print(f"- Тег уже существует: {tag.name}")

print("\n✅ Готово! Категории и теги добавлены.")
print("Теперь можете назначить их фотографиям через админ-панель.")
