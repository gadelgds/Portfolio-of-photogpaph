"""
Скрипт для смены пароля администратора
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User

# Показываем всех существующих пользователей
print("=" * 60)
print("Существующие пользователи:")
print("=" * 60)

users = User.objects.all()
if users:
    for user in users:
        status = "✓ Админ" if user.is_superuser else "  Обычный"
        print(f"{status} | Логин: {user.username} | Email: {user.email}")
else:
    print("❌ Пользователей не найдено!")

print("=" * 60)

# Если есть хотя бы один пользователь, меняем пароль
if users:
    print("\nВведи данные для смены пароля:")
    username = input("Логин пользователя: ").strip()
    
    try:
        user = User.objects.get(username=username)
        new_password = input("Новый пароль: ").strip()
        
        user.set_password(new_password)
        user.save()
        
        print(f"\n✅ Пароль для пользователя '{username}' успешно изменен!")
        print(f"Теперь можешь войти:")
        print(f"  Логин: {username}")
        print(f"  Пароль: {new_password}")
        
    except User.DoesNotExist:
        print(f"\n❌ Пользователь '{username}' не найден!")
else:
    print("\n💡 Создай нового администратора командой:")
    print("   python manage.py createsuperuser")
