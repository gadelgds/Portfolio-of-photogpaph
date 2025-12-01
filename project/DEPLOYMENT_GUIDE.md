# Инструкция по развертыванию проекта на новом компьютере

## Шаг 1: Установка необходимого ПО

### 1.1 Установите Python (если не установлен)
- Скачайте Python 3.10+ с https://www.python.org/downloads/
- При установке отметьте "Add Python to PATH"
- Проверьте: `python --version`

### 1.2 Установите PostgreSQL
- Скачайте с https://www.postgresql.org/download/
- Запустите установщик
- **ВАЖНО:** Запомните пароль для пользователя `postgres`
- Порт по умолчанию: `5432`
- Проверьте: `psql --version`

### 1.3 Установите Git (если нужно клонировать проект)
- Скачайте с https://git-scm.com/downloads

---

## Шаг 2: Получение проекта

### Вариант А: Копирование файлов
Скопируйте всю папку проекта на новый компьютер

### Вариант Б: Клонирование из Git
```bash
git clone <ссылка-на-репозиторий>
cd Portfolio-of-photogpaph
```

---

## Шаг 3: Создание виртуального окружения

```bash
# Перейдите в папку проекта
cd Portfolio-of-photogpaph

# Создайте виртуальное окружение
python -m venv venv

# Активируйте его
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

После активации вы увидите `(venv)` в начале строки командной строки.

---

## Шаг 4: Установка зависимостей Python

```bash
cd project
pip install -r requirements.txt
```

Это установит:
- Django
- psycopg2-binary (драйвер PostgreSQL)
- Pillow (для работы с изображениями)

---

## Шаг 5: Настройка PostgreSQL

### 5.1 Создайте базу данных

Откройте командную строку PostgreSQL:

```bash
# Windows (через меню Пуск найдите "SQL Shell (psql)")
# Или через командную строку:
psql -U postgres
```

Введите пароль, который вы установили при установке PostgreSQL.

Создайте базу данных:
```sql
CREATE DATABASE photographer_db;
\q
```

### 5.2 Обновите настройки подключения

**Вариант А: Автоматически (рекомендуется)**
```bash
python setup_postgresql.py
```

Скрипт спросит:
- Название базы данных (нажмите Enter для `photographer_db`)
- Имя пользователя (нажмите Enter для `postgres`)
- Пароль PostgreSQL (введите ваш пароль)
- Хост (нажмите Enter для `localhost`)
- Порт (нажмите Enter для `5432`)

**Вариант Б: Вручную**

Откройте файл `project/project/settings.py` и найдите раздел `DATABASES`:

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

Замените `'your_password'` на ваш реальный пароль PostgreSQL.

---

## Шаг 6: Применение миграций

```bash
python manage.py migrate
```

Вы должны увидеть:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, game, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

---

## Шаг 7: Создание суперпользователя (администратора)

```bash
python manage.py createsuperuser
```

Введите:
- Имя пользователя
- Email (можно оставить пустым)
- Пароль (можно простой, например "admin")

---

## Шаг 8: Сбор статических файлов (опционально для production)

```bash
python manage.py collectstatic
```

---

## Шаг 9: Запуск сервера

```bash
python manage.py runserver
```

Откройте браузер и перейдите на:
- **Сайт:** http://127.0.0.1:8000/
- **Админка:** http://127.0.0.1:8000/admin/

---

## Шаг 10: Добавление тестовых данных (опционально)

Если у вас есть скрипты для добавления данных:

```bash
# Добавить категории и теги
python add_categories_tags.py

# Добавить тестовые отзывы
python add_test_reviews.py
```

---

## Быстрая шпаргалка (для опытных)

```bash
# 1. Установите PostgreSQL и создайте БД
psql -U postgres
CREATE DATABASE photographer_db;
\q

# 2. Настройте проект
cd Portfolio-of-photogpaph
python -m venv venv
venv\Scripts\activate  # Windows
cd project
pip install -r requirements.txt

# 3. Настройте подключение к БД
python setup_postgresql.py

# 4. Примените миграции
python manage.py migrate

# 5. Создайте суперпользователя
python manage.py createsuperuser

# 6. Запустите сервер
python manage.py runserver
```

---

## Возможные проблемы и решения

### ❌ Ошибка: "psycopg2 not found"
```bash
pip install psycopg2-binary
```

### ❌ Ошибка: "FATAL: password authentication failed"
- Проверьте пароль в `settings.py`
- Убедитесь, что используете правильный пароль PostgreSQL

### ❌ Ошибка: "database does not exist"
```bash
psql -U postgres
CREATE DATABASE photographer_db;
\q
```

### ❌ Ошибка: "No module named 'PIL'"
```bash
pip install Pillow
```

### ❌ PostgreSQL не запускается
**Windows:**
- Откройте "Службы" (services.msc)
- Найдите "postgresql-x64-XX"
- Нажмите "Запустить"

**Linux:**
```bash
sudo systemctl start postgresql
```

### ❌ Порт 8000 уже занят
```bash
python manage.py runserver 8001
```

---

## Перенос данных со старого компьютера

Если нужно перенести данные (фотографии, заказы, отзывы):

### На старом компьютере:
```bash
# Экспорт данных
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > data.json

# Скопируйте файл data.json на новый компьютер
```

### На новом компьютере:
```bash
# После выполнения миграций:
python manage.py loaddata data.json
```

### Перенос медиа файлов:
Скопируйте папку `project/media/` со старого компьютера на новый.

---

## Проверка работоспособности

✅ Сервер запустился без ошибок
✅ Открывается главная страница http://127.0.0.1:8000/
✅ Можно войти в админку http://127.0.0.1:8000/admin/
✅ Отображаются фотографии (если были загружены)
✅ Работает регистрация и вход пользователей

---

## Дополнительные команды

```bash
# Создать нового суперпользователя
python manage.py createsuperuser

# Проверить подключение к БД
python manage.py dbshell

# Очистить все данные из БД (ОСТОРОЖНО!)
python manage.py flush

# Создать новые миграции (если изменили models.py)
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Запустить тесты
python manage.py test
```

---

## Контрольный список развертывания

- [ ] Python установлен
- [ ] PostgreSQL установлен и запущен
- [ ] Виртуальное окружение создано и активировано
- [ ] Зависимости установлены (`pip install -r requirements.txt`)
- [ ] База данных создана (`CREATE DATABASE photographer_db`)
- [ ] Настройки подключения обновлены (`settings.py`)
- [ ] Миграции применены (`python manage.py migrate`)
- [ ] Суперпользователь создан (`python manage.py createsuperuser`)
- [ ] Сервер запускается (`python manage.py runserver`)
- [ ] Сайт открывается в браузере

---

## Полезные ссылки

- Django документация: https://docs.djangoproject.com/
- PostgreSQL документация: https://www.postgresql.org/docs/
- Python документация: https://docs.python.org/

---

**Готово!** Ваш проект должен работать на новом компьютере.

Если возникли проблемы, проверьте:
1. Запущен ли PostgreSQL
2. Правильный ли пароль в settings.py
3. Активировано ли виртуальное окружение
4. Установлены ли все зависимости
