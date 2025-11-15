"""
Скрипт для быстрого создания администратора
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User

print("=" * 60)
print("СОЗДАНИЕ АДМИНИСТРАТОРА")
print("=" * 60)

# Проверяем существующих пользователей
existing_users = User.objects.all()
if existing_users:
    print("\nСуществующие пользователи:")
    for user in existing_users:
        status = "✓ Админ" if user.is_superuser else "  Обычный"
        print(f"{status} | Логин: {user.username}")
    print()

# Вводим данные
username = input("Введи логин (например: admin): ").strip() or "admin"
email = input("Введи email (можно пропустить): ").strip() or ""
password = input("Введи пароль (например: admin123): ").strip() or "admin123"

# Проверяем, не существует ли уже такой пользователь
if User.objects.filter(username=username).exists():
    print(f"\n⚠️  Пользователь '{username}' уже существует!")
    choice = input("Хочешь изменить его пароль? (да/нет): ").strip().lower()
    
    if choice in ['да', 'yes', 'y', 'д']:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"\n✅ Пароль для '{username}' изменен!")
    else:
        print("\n❌ Отменено")
        exit()
else:
    # Создаем нового суперпользователя
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"\n✅ Администратор успешно создан!")

print("\n" + "=" * 60)
print("ДАННЫЕ ДЛЯ ВХОДА:")
print("=" * 60)
print(f"URL:    http://localhost:8000/admin/")
print(f"Логин:  {username}")
print(f"Пароль: {password}")
print("=" * 60)
print("\n💡 Сохрани эти данные!")
