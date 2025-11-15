"""
Автоматическое создание администратора
Логин: admin
Пароль: admin123
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User

print("=" * 60)
print("АВТОМАТИЧЕСКОЕ СОЗДАНИЕ АДМИНИСТРАТОРА")
print("=" * 60)

username = "admin"
password = "admin123"
email = "admin@example.com"

# Удаляем старого админа, если есть
if User.objects.filter(username=username).exists():
    User.objects.filter(username=username).delete()
    print(f"⚠️  Старый пользователь '{username}' удален")

# Создаем нового
user = User.objects.create_superuser(
    username=username,
    email=email,
    password=password
)

print(f"✅ Администратор успешно создан!")
print("\n" + "=" * 60)
print("ДАННЫЕ ДЛЯ ВХОДА В АДМИН-ПАНЕЛЬ:")
print("=" * 60)
print(f"URL:    http://localhost:8000/admin/")
print(f"Логин:  {username}")
print(f"Пароль: {password}")
print("=" * 60)
print("\n💡 Сохрани эти данные в надежном месте!")
print("💡 После входа можешь сменить пароль в админке")
