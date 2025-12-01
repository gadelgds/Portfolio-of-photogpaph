# Быстрый старт на новом компьютере

## Минимальные требования
- Python 3.10+
- PostgreSQL 12+

---

## 5 минут до запуска

### 1️⃣ Установите PostgreSQL и создайте БД
```bash
psql -U postgres
CREATE DATABASE photographer_db;
\q
```

### 2️⃣ Настройте Python окружение
```bash
cd Portfolio-of-photogpaph
python -m venv venv
venv\Scripts\activate
cd project
pip install -r requirements.txt
```

### 3️⃣ Настройте подключение к БД
```bash
python setup_postgresql.py
```
Или вручную отредактируйте `project/settings.py` (строка 82) - укажите пароль PostgreSQL.

### 4️⃣ Примените миграции и создайте админа
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5️⃣ Запустите сервер
```bash
python manage.py runserver
```

**Готово!** Откройте http://127.0.0.1:8000/

---

## Что делать если что-то не работает?

### PostgreSQL не установлен?
Скачайте: https://www.postgresql.org/download/

### Ошибка "psycopg2 not found"?
```bash
pip install psycopg2-binary
```

### Ошибка "password authentication failed"?
Проверьте пароль в `project/project/settings.py` (строка 86)

### База данных не создана?
```bash
psql -U postgres
CREATE DATABASE photographer_db;
\q
```

---

## Структура проекта

```
Portfolio-of-photogpaph/
├── project/
│   ├── manage.py              # Главный файл Django
│   ├── requirements.txt       # Зависимости Python
│   ├── setup_postgresql.py    # Скрипт настройки БД
│   ├── project/
│   │   └── settings.py        # Настройки (ЗДЕСЬ ПАРОЛЬ БД!)
│   ├── game/                  # Основное приложение
│   ├── templates/             # HTML шаблоны
│   ├── static/                # CSS, JS
│   └── media/                 # Загруженные файлы
└── README.md
```

---

## Важные файлы

| Файл | Зачем нужен |
|------|-------------|
| `requirements.txt` | Список Python пакетов для установки |
| `settings.py` | Настройки Django (БД, пароли, пути) |
| `manage.py` | Команды Django (migrate, runserver и т.д.) |
| `setup_postgresql.py` | Автоматическая настройка PostgreSQL |

---

## Полезные команды

```bash
# Активировать виртуальное окружение
venv\Scripts\activate

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver

# Запустить на другом порту
python manage.py runserver 8001
```

---

## Нужна подробная инструкция?

Смотрите файл `DEPLOYMENT_GUIDE.md` - там все расписано пошагово с решением проблем.
