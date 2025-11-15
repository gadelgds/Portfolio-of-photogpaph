# 📄 Как работают HTML шаблоны в Django

## 🏗️ Структура шаблонов

В твоем проекте используется **система наследования шаблонов**. Это как конструктор:

```
base.html (основа)
    ├── home.html (главная)
    ├── services.html (услуги)
    └── reviews.html (отзывы)
```

---

## 📋 1. BASE.HTML - Главный шаблон (основа)

Это **родительский шаблон** - основа для всех страниц.

### Что в нем есть:

```html
{% load static %}  <!-- Подключение статических файлов -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Сайт фотографа{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>
<body>
    <!-- Шапка (одинаковая на всех страницах) -->
    <div class="header">
        <h1>📷 Фотограф Алексей</h1>
    </div>
    
    <!-- Меню (одинаковое на всех страницах) -->
    <div class="menu">
        <a href="{% url 'home' %}">Главная</a>
        <a href="{% url 'services' %}">Услуги</a>
        <a href="{% url 'reviews' %}">Отзывы</a>
    </div>
    
    <!-- БЛОК КОНТЕНТА (меняется на каждой странице) -->
    <div class="content">
        {% block content %}
        {% endblock %}
    </div>
    
    <!-- Подвал (одинаковый на всех страницах) -->
    <div class="footer">
        <p>© 2024 Фотограф Алексей</p>
    </div>
</body>
</html>
```

### Ключевые элементы:

**`{% load static %}`** - подключает систему статических файлов (CSS, JS, картинки)

**`{% block title %}`** - блок для заголовка страницы (можно переопределить)

**`{% block content %}`** - блок для основного контента (обязательно переопределяется)

**`{% url 'home' %}`** - генерирует URL по имени маршрута

**`{% static 'css/styles.css' %}`** - путь к статическому файлу

---

## 🏠 2. HOME.HTML - Главная страница

Это **дочерний шаблон** - наследует base.html и заполняет блок content.

```html
{% extends 'game/base.html' %}  <!-- Наследуем base.html -->

{% block content %}  <!-- Заполняем блок content -->
<h2>Мое портфолио</h2>

<div class="gallery">
    {% for photo in photos %}  <!-- Цикл по фотографиям -->
    <div class="photo-card">
        <img src="{{ photo.image.url }}" alt="{{ photo.title }}">
        <h3>{{ photo.title }}</h3>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

### Что происходит:

1. Django берет `base.html`
2. Находит `{% block content %}`
3. Вставляет туда содержимое из `home.html`
4. Получается полная страница с шапкой, меню, контентом и подвалом

---

## 💬 3. REVIEWS.HTML - Страница отзывов

```html
{% extends 'game/base.html' %}
{% load static %}

{% block title %}Отзывы клиентов{% endblock %}  <!-- Меняем заголовок -->

{% block content %}
<h1>💬 Отзывы наших клиентов</h1>

<!-- Условие: если есть сообщения -->
{% if messages %}
    {% for message in messages %}
        <div class="alert">{{ message }}</div>
    {% endfor %}
{% endif %}

<!-- Условие: если есть отзывы -->
{% if reviews %}
    {% for review in reviews %}  <!-- Цикл по отзывам -->
        <div class="review-card">
            <span>{{ review.author_name }}</span>
            <p>{{ review.text }}</p>
        </div>
    {% endfor %}
{% else %}
    <p>Пока нет отзывов</p>
{% endif %}

<!-- Форма -->
<form method="post">
    {% csrf_token %}  <!-- Защита от CSRF -->
    {{ form.author_name }}
    <button type="submit">Отправить</button>
</form>
{% endblock %}
```

---

## 🎯 Основные теги Django

### 1. Наследование и блоки

```django
{% extends 'game/base.html' %}  - наследовать шаблон
{% block название %}...{% endblock %}  - определить блок
```

### 2. Переменные

```django
{{ переменная }}  - вывести значение
{{ photo.title }}  - вывести поле объекта
{{ photo.image.url }}  - вывести URL картинки
```

### 3. Циклы

```django
{% for item in items %}
    {{ item.name }}
{% endfor %}

{% for item in items %}
    {{ forloop.counter }}  - номер итерации (1, 2, 3...)
{% endfor %}
```

### 4. Условия

```django
{% if условие %}
    Текст если True
{% else %}
    Текст если False
{% endif %}

{% if reviews %}  - если список не пустой
{% if user.is_authenticated %}  - если пользователь авторизован
```

### 5. Фильтры

```django
{{ text|upper }}  - в верхний регистр
{{ date|date:"d.m.Y" }}  - форматировать дату
{{ price|floatformat:2 }}  - 2 знака после запятой
{{ text|truncatewords:10 }}  - обрезать до 10 слов
```

### 6. Статические файлы

```django
{% load static %}  - подключить систему
{% static 'css/styles.css' %}  - путь к файлу
<img src="{% static 'images/logo.png' %}">
```

### 7. URL

```django
{% url 'home' %}  - URL по имени
{% url 'photo_detail' photo.id %}  - URL с параметром
<a href="{% url 'reviews' %}">Отзывы</a>
```

### 8. Формы

```django
{% csrf_token %}  - токен безопасности (обязательно!)
{{ form.field_name }}  - поле формы
{{ form.field_name.label }}  - метка поля
{{ form.field_name.errors }}  - ошибки поля
```

---

## 🔄 Как данные попадают в шаблон

### Путь данных:

```
База данных → Model → View → Template → Браузер
```

### Пример:

**1. Model (models.py):**
```python
class Review(models.Model):
    author_name = models.CharField(max_length=100)
    text = models.TextField()
```

**2. View (views.py):**
```python
def reviews(request):
    reviews = Review.objects.all()  # Получаем из БД
    return render(request, 'game/reviews.html', {
        'reviews': reviews  # Передаем в шаблон
    })
```

**3. Template (reviews.html):**
```html
{% for review in reviews %}
    <p>{{ review.author_name }}: {{ review.text }}</p>
{% endfor %}
```

---

## ➕ Как добавить новый элемент на страницу

### Пример 1: Добавить секцию "О нас" на главную

**Открой `home.html` и добавь:**

```html
{% extends 'game/base.html' %}

{% block content %}
<h2>Мое портфолио</h2>
<!-- ... существующий код ... -->

<!-- НОВАЯ СЕКЦИЯ -->
<div style="background: white; padding: 30px; border-radius: 8px; margin-top: 30px;">
    <h2>👨‍💼 Обо мне</h2>
    <p>Меня зовут Алексей, я профессиональный фотограф с опытом более 5 лет.</p>
    <p>Специализируюсь на:</p>
    <ul>
        <li>Свадебной фотографии</li>
        <li>Портретной съемке</li>
        <li>Семейных фотосессиях</li>
    </ul>
</div>
{% endblock %}
```

### Пример 2: Добавить контактную форму

**Создай новый файл `templates/game/contact.html`:**

```html
{% extends 'game/base.html' %}

{% block title %}Контакты{% endblock %}

{% block content %}
<h1>📞 Свяжитесь со мной</h1>

<div style="background: white; padding: 30px; border-radius: 8px;">
    <h2>Контактная информация</h2>
    <p><strong>Телефон:</strong> +7 (999) 123-45-67</p>
    <p><strong>Email:</strong> photo@example.com</p>
    <p><strong>Адрес:</strong> Москва, ул. Примерная, д. 1</p>
    
    <h3>Напишите мне</h3>
    <form method="post">
        {% csrf_token %}
        <div style="margin-bottom: 15px;">
            <label>Ваше имя:</label>
            <input type="text" name="name" class="form-control" required>
        </div>
        <div style="margin-bottom: 15px;">
            <label>Email:</label>
            <input type="email" name="email" class="form-control" required>
        </div>
        <div style="margin-bottom: 15px;">
            <label>Сообщение:</label>
            <textarea name="message" class="form-control" rows="5" required></textarea>
        </div>
        <button type="submit" class="btn-submit">Отправить</button>
    </form>
</div>
{% endblock %}
```

**Добавь в `urls.py`:**
```python
path('contact/', views.contact, name='contact'),
```

**Добавь в `views.py`:**
```python
def contact(request):
    if request.method == 'POST':
        # Обработка формы
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        messages.success(request, 'Спасибо! Мы свяжемся с вами.')
        return redirect('contact')
    return render(request, 'game/contact.html')
```

**Добавь ссылку в меню (`base.html`):**
```html
<div class="menu">
    <a href="{% url 'home' %}">Главная</a>
    <a href="{% url 'services' %}">Услуги</a>
    <a href="{% url 'reviews' %}">Отзывы</a>
    <a href="{% url 'contact' %}">Контакты</a>  <!-- НОВАЯ ССЫЛКА -->
</div>
```

### Пример 3: Добавить счетчик отзывов

**В `reviews.html` добавь перед списком отзывов:**

```html
<div style="background: #e8f4f8; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
    <p style="margin: 0; font-size: 18px;">
        📊 Всего отзывов: <strong>{{ reviews|length }}</strong>
    </p>
</div>
```

### Пример 4: Добавить кнопку "Наверх"

**В `base.html` перед закрывающим `</body>`:**

```html
<!-- Кнопка "Наверх" -->
<button onclick="window.scrollTo(0,0)" 
        style="position: fixed; bottom: 20px; right: 20px; 
               background: #3498db; color: white; border: none; 
               padding: 15px; border-radius: 50%; cursor: pointer; 
               font-size: 20px;">
    ↑
</button>
</body>
```

---

## 🎨 Как добавить стили

### Вариант 1: Inline стили (прямо в HTML)

```html
<div style="background: white; padding: 20px; border-radius: 8px;">
    Контент
</div>
```

### Вариант 2: В styles.css (правильный способ)

**1. Добавь в `static/css/styles.css`:**
```css
.contact-info {
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

**2. Используй в HTML:**
```html
<div class="contact-info">
    Контент
</div>
```

---

## 📝 Чек-лист: Как добавить новую страницу

1. **Создай HTML шаблон** в `templates/game/`
   ```html
   {% extends 'game/base.html' %}
   {% block content %}
   <!-- Твой контент -->
   {% endblock %}
   ```

2. **Создай функцию в `views.py`**
   ```python
   def my_page(request):
       return render(request, 'game/my_page.html')
   ```

3. **Добавь маршрут в `urls.py`**
   ```python
   path('my-page/', views.my_page, name='my_page'),
   ```

4. **Добавь ссылку в меню (`base.html`)**
   ```html
   <a href="{% url 'my_page' %}">Моя страница</a>
   ```

---

## 🔍 Полезные советы

### 1. Комментарии в шаблонах

```django
{# Это комментарий - не отображается в браузере #}

{% comment %}
Многострочный
комментарий
{% endcomment %}
```

### 2. Отладка - вывести все переменные

```django
{{ request }}  - информация о запросе
{{ user }}  - текущий пользователь
```

### 3. Проверка на пустоту

```django
{% if reviews %}
    Есть отзывы
{% else %}
    Нет отзывов
{% endif %}

{% if not reviews %}
    Список пустой
{% endif %}
```

### 4. Множественные условия

```django
{% if user.is_authenticated and user.is_staff %}
    Админ-панель
{% endif %}
```

---

## 🎯 Что куратор может попросить добавить

### 1. Галерея с фильтрацией
```html
<div>
    <button onclick="filterPhotos('all')">Все</button>
    <button onclick="filterPhotos('wedding')">Свадьбы</button>
    <button onclick="filterPhotos('portrait')">Портреты</button>
</div>
```

### 2. Форма обратной связи
```html
<form method="post">
    {% csrf_token %}
    <input type="text" name="name" placeholder="Имя">
    <input type="email" name="email" placeholder="Email">
    <textarea name="message" placeholder="Сообщение"></textarea>
    <button type="submit">Отправить</button>
</form>
```

### 3. Счетчики и статистика
```html
<div>
    <p>Фотографий: {{ photos|length }}</p>
    <p>Отзывов: {{ reviews|length }}</p>
    <p>Услуг: {{ services|length }}</p>
</div>
```

### 4. Хлебные крошки (навигация)
```html
<div style="margin-bottom: 20px;">
    <a href="{% url 'home' %}">Главная</a> / 
    <span>Отзывы</span>
</div>
```

### 5. Социальные сети
```html
<div class="social-links">
    <a href="https://vk.com/yourpage">VK</a>
    <a href="https://instagram.com/yourpage">Instagram</a>
    <a href="https://t.me/yourpage">Telegram</a>
</div>
```

---

## ✅ Главное запомнить

1. **`base.html`** - основа, содержит шапку, меню, подвал
2. **Другие шаблоны** - наследуют base.html через `{% extends %}`
3. **`{% block content %}`** - место для уникального контента страницы
4. **`{{ переменная }}`** - вывод данных из Python
5. **`{% for %}`** - циклы для списков
6. **`{% if %}`** - условия
7. **`{% url %}`** - генерация ссылок
8. **`{% csrf_token %}`** - обязательно в формах!

---

Теперь ты можешь легко добавлять новые элементы на страницы! 🚀
