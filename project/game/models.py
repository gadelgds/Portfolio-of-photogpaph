from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    """Категории для фотографий (портрет, пейзаж, свадьба и т.д.)"""
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    """Теги для фотографий"""
    name = models.CharField(max_length=50, verbose_name='Название')
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self):
        return self.name

class Photo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/')
    preview = models.ImageField(upload_to='previews/', blank=True)  # Опционально
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0, verbose_name='Лайки')  # Количество лайков
    views = models.IntegerField(default=0, verbose_name='Просмотры')  # Количество просмотров
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='photos', verbose_name='Теги')

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Review(models.Model):
    """Модель для хранения отзывов пользователей"""
    # Связь с фотографией (опционально - может быть общий отзыв о работе)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True, verbose_name='Фотография')
    
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

class PhotoLike(models.Model):
    """Модель для отслеживания лайков и предотвращения накрутки"""
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='photo_likes', verbose_name='Фотография')
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    
    class Meta:
        unique_together = ['photo', 'ip_address']  # Один IP = один лайк на фото
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
    
    def __str__(self):
        return f'Лайк от {self.ip_address} для {self.photo.title}'

class Order(models.Model):
    """Модель для заказов услуг фотографа"""
    
    # Статусы заказа
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтвержден'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]
    
    # Информация о клиенте
    client_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    client_email = models.EmailField(verbose_name='Email клиента')
    client_phone = models.CharField(max_length=20, verbose_name='Телефон клиента')
    
    # Связь с услугой
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='orders', verbose_name='Услуга')
    
    # Даты
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    shoot_date = models.DateField(verbose_name='Дата съемки')
    
    # Статус и сумма
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    
    # Дополнительная информация
    notes = models.TextField(blank=True, verbose_name='Комментарий клиента')
    
    class Meta:
        ordering = ['-order_date']  # Сортировка: новые сверху
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self):
        return f'Заказ #{self.id} от {self.client_name} - {self.get_status_display()}'

class UserProfile(models.Model):
    """Расширенный профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f'Профиль {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создаем профиль при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняем профиль при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
