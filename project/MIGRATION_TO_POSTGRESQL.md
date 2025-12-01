# Миграция на PostgreSQL

## Шаг 1: Установка PostgreSQL

### Windows:
1. Скачайте PostgreSQL с официального сайта: https://www.postgresql.org/download/windows/
2. Запустите установщик
3. Запомните пароль для пользователя `postgres`
4. Порт по умолчанию: `5432`

### Проверка установки:
```bash
psql --version
```

## Шаг 2: Создание базы данных

Откройте командную строку PostgreSQL (psql) или pgAdmin и выполните:

```sql
CREATE DATABASE photographer_db;
```

Или через командную строку:
```bash
psql -U postgres
CREATE DATABASE photographer_db;
\q
```

## Шаг 3: Установка Python пакетов

```bash
pip install psycopg2-binary
```

Или установите все зависимости:
```bash
pip install -r requirements.txt
```

## Шаг 4: Обновление настроек

В файле `project/settings.py` уже настроено подключение к PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'photographer_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',  # ЗАМЕНИТЕ НА ВАШ ПАРОЛЬ!
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**ВАЖНО:** Замените `'your_password'` на ваш реальный пароль PostgreSQL!

## Шаг 5: Применение миграций

```bash
cd project
python manage.py migrate
```

## Шаг 6: Создание суперпользователя

```bash
python manage.py createsuperuser
```

## Шаг 7: Перенос данных (опционально)

Если нужно перенести данные из SQLite:

### Экспорт данных из SQLite:
```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > data.json
```

### Импорт данных в PostgreSQL:
```bash
python manage.py loaddata data.json
```

## Шаг 8: Запуск сервера

```bash
python manage.py runserver
```

## Проверка подключения

Если все настроено правильно, вы увидите:
```
System check identified no issues (0 silenced).
Django version X.X.X, using settings 'project.settings'
Starting development server at http://127.0.0.1:8000/
```

## Возможные проблемы

### Ошибка: "psycopg2 not found"
```bash
pip install psycopg2-binary
```

### Ошибка: "FATAL: password authentication failed"
- Проверьте пароль в settings.py
- Убедитесь, что пользователь postgres существует

### Ошибка: "database does not exist"
```bash
psql -U postgres
CREATE DATABASE photographer_db;
```

### Ошибка подключения к серверу PostgreSQL
- Убедитесь, что PostgreSQL запущен
- Проверьте порт (по умолчанию 5432)

## Преимущества PostgreSQL

✅ Лучшая производительность для больших объемов данных
✅ Поддержка сложных запросов
✅ ACID-совместимость
✅ Расширенные возможности индексирования
✅ Подходит для production
✅ Поддержка JSON полей
✅ Полнотекстовый поиск

## Откат на SQLite (если нужно)

Просто измените в settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
