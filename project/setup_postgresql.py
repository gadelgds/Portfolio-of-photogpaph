"""
Скрипт для настройки PostgreSQL
Запустите этот скрипт для автоматической настройки базы данных
"""

import os
import sys
import getpass

def update_settings():
    """Обновляет settings.py с учетными данными PostgreSQL"""
    
    print("=" * 50)
    print("Настройка PostgreSQL для Django проекта")
    print("=" * 50)
    
    # Получаем данные от пользователя
    db_name = input("Название базы данных [photographer_db]: ").strip() or "photographer_db"
    db_user = input("Имя пользователя PostgreSQL [postgres]: ").strip() or "postgres"
    db_password = getpass.getpass("Пароль PostgreSQL: ")
    db_host = input("Хост [localhost]: ").strip() or "localhost"
    db_port = input("Порт [5432]: ").strip() or "5432"
    
    # Путь к settings.py
    settings_path = os.path.join(os.path.dirname(__file__), 'project', 'settings.py')
    
    # Читаем файл
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем настройки базы данных
    old_db_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'photographer_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',  # Замените на ваш пароль PostgreSQL
        'HOST': 'localhost',
        'PORT': '5432',
    }
}"""
    
    new_db_config = f"""DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{db_name}',
        'USER': '{db_user}',
        'PASSWORD': '{db_password}',
        'HOST': '{db_host}',
        'PORT': '{db_port}',
    }}
}}"""
    
    content = content.replace(old_db_config, new_db_config)
    
    # Сохраняем файл
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ Настройки обновлены!")
    print(f"\nБаза данных: {db_name}")
    print(f"Пользователь: {db_user}")
    print(f"Хост: {db_host}:{db_port}")
    
    print("\n" + "=" * 50)
    print("Следующие шаги:")
    print("=" * 50)
    print("1. Убедитесь, что PostgreSQL запущен")
    print(f"2. Создайте базу данных: CREATE DATABASE {db_name};")
    print("3. Установите psycopg2: pip install psycopg2-binary")
    print("4. Примените миграции: python manage.py migrate")
    print("5. Создайте суперпользователя: python manage.py createsuperuser")
    print("6. Запустите сервер: python manage.py runserver")

if __name__ == '__main__':
    try:
        update_settings()
    except KeyboardInterrupt:
        print("\n\nОтменено пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)
