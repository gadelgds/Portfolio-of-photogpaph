from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Photo, Service, Review
from .forms import ReviewForm

def home(request):
    photos = Photo.objects.all()
    return render(request, 'game/home.html', {'photos': photos})

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'game/photo_detail.html', {'photo': photo})

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