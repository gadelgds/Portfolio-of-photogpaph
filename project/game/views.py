from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import Photo, Service, Review, PhotoLike, Category, Order
from .forms import ReviewForm, OrderForm

def home(request):
    # Получаем все категории для фильтра
    categories = Category.objects.all()
    
    # Проверяем, выбрана ли категория
    category_slug = request.GET.get('category')
    
    if category_slug:
        # Фильтруем по категории
        photos = Photo.objects.filter(category__slug=category_slug).order_by('-views')
        selected_category = Category.objects.get(slug=category_slug)
    else:
        # Показываем все фотографии
        photos = Photo.objects.all().order_by('-views')
        selected_category = None
    
    context = {
        'photos': photos,
        'categories': categories,
        'selected_category': selected_category
    }
    return render(request, 'game/home.html', context)

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    
    # Увеличиваем счетчик просмотров при каждом открытии страницы
    photo.views += 1
    photo.save()
    
    # Получаем одобренные отзывы для этой фотографии
    photo_reviews = photo.reviews.filter(is_approved=True)
    
    # Обработка формы комментария
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Сохраняем отзыв, но не сразу в БД
            review = form.save(commit=False)
            # Привязываем отзыв к этой фотографии
            review.photo = photo
            # По умолчанию отзыв не одобрен (нужна модерация)
            review.is_approved = False
            review.save()
            
            # Показываем сообщение пользователю
            messages.success(request, '💬 Спасибо за комментарий! Он появится после модерации.')
            
            # Перенаправляем на эту же страницу (чтобы форма очистилась)
            return redirect('photo_detail', photo_id=photo_id)
    else:
        # Если GET запрос - просто показываем пустую форму
        form = ReviewForm()
    
    context = {
        'photo': photo,
        'photo_reviews': photo_reviews,
        'form': form
    }
    return render(request, 'game/photo_detail.html', context)

def services(request):
    services = Service.objects.all()
    return render(request, 'game/services.html', {'services': services})

def reviews(request):
    """
    Страница отзывов
    Показывает все одобренные отзывы и форму для добавления нового
    """
    # Получаем только одобренные отзывы
    approved_reviews = Review.objects.filter(is_approved=True)
    
    # Обработка формы при отправке (POST запрос)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Сохраняем отзыв, но не сразу в БД
            review = form.save(commit=False)
            # По умолчанию отзыв не одобрен (нужна модерация)
            review.is_approved = False
            review.save()
            
            # Показываем сообщение пользователю
            messages.success(request, 'Спасибо за отзыв! Он появится после модерации.')
            
            # Перенаправляем на эту же страницу (чтобы форма очистилась)
            return redirect('reviews')
    else:
        # Если GET запрос - просто показываем пустую форму
        form = ReviewForm()
    
    # Передаем данные в шаблон
    context = {
        'reviews': approved_reviews,
        'form': form
    }
    return render(request, 'game/reviews.html', context)

def contact(request):
    """
    Страница контактов
    """
    return render(request, 'game/contact.html')

def like_photo(request, photo_id):
    """
    Обработка лайка фотографии с защитой от накрутки
    """
    photo = get_object_or_404(Photo, id=photo_id)
    
    # Получаем IP адрес пользователя
    ip_address = get_client_ip(request)
    
    try:
        # Пытаемся создать запись о лайке
        PhotoLike.objects.create(photo=photo, ip_address=ip_address)
        
        # Увеличиваем счетчик лайков
        photo.likes += 1
        photo.save()
        
        messages.success(request, '❤️ Спасибо за лайк!')
    except IntegrityError:
        # Если этот IP уже лайкал эту фотографию
        messages.warning(request, 'Вы уже поставили лайк этой фотографии!')
    
    # Перенаправляем обратно на страницу фотографии
    return redirect('photo_detail', photo_id=photo_id)

def get_client_ip(request):
    """Получение IP адреса клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def create_order(request, service_id):
    """
    Создание заказа на услугу
    """
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Сохраняем заказ, но не сразу в БД
            order = form.save(commit=False)
            # Привязываем к услуге
            order.service = service
            # Устанавливаем сумму из цены услуги
            order.total_amount = service.price
            order.save()
            
            # Показываем сообщение пользователю
            messages.success(request, f'✅ Заказ #{order.id} успешно создан! Мы свяжемся с вами в ближайшее время.')
            
            # Перенаправляем на страницу услуг
            return redirect('services')
    else:
        # Если GET запрос - просто показываем пустую форму
        form = OrderForm()
    
    context = {
        'form': form,
        'service': service
    }
    return render(request, 'game/create_order.html', context)