from django.db import models
class Photo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/')
    preview = models.ImageField(upload_to='previews/', blank=True)  # Опционально
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Review(models.Model):
    """Модель для хранения отзывов пользователей"""
    # Имя автора отзыва
    author_name = models.CharField(max_length=100, verbose_name='Имя')
    
    # Email (необязательное поле)
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    
    # Оценка от 1 до 5
    rating = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        verbose_name='Оценка'
    )
    
    # Текст отзыва
    text = models.TextField(verbose_name='Отзыв')
    
    # Дата создания (автоматически)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    
    # Одобрен ли отзыв модератором (по умолчанию False)
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')
    
    class Meta:
        ordering = ['-created_at']  # Сортировка: новые сверху
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    
    def __str__(self):
        return f'Отзыв от {self.author_name} - {self.rating}★'
# Create your models here.
