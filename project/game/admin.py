from django.contrib import admin
from .models import Photo, Service, Review, Category, Tag, PhotoLike, Order

# Регистрация Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в админ-панели"""
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# Регистрация Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройка отображения тегов в админ-панели"""
    list_display = ['name']
    search_fields = ['name']

# Расширенная регистрация Photo
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Настройка отображения фотографий в админ-панели"""
    list_display = ['title', 'category', 'likes', 'views', 'uploaded_at']
    list_filter = ['uploaded_at', 'category', 'tags']
    search_fields = ['title']
    readonly_fields = ['likes', 'views', 'uploaded_at']
    filter_horizontal = ['tags']  # Удобный виджет для выбора тегов

# Регистрация Service
admin.site.register(Service)

# Регистрация PhotoLike
@admin.register(PhotoLike)
class PhotoLikeAdmin(admin.ModelAdmin):
    """Настройка отображения лайков в админ-панели"""
    list_display = ['photo', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['ip_address', 'photo__title']
    readonly_fields = ['photo', 'ip_address', 'created_at']

# Регистрация Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Настройка отображения заказов в админ-панели"""
    list_display = ['id', 'client_name', 'service', 'shoot_date', 'status', 'total_amount', 'order_date', 'notes']
    list_filter = ['status', 'order_date', 'shoot_date']
    search_fields = ['client_name', 'client_email', 'client_phone', 'notes']
    list_editable = ['status']  # Можно менять статус прямо в списке
    readonly_fields = ['order_date', 'total_amount']
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('client_name', 'client_email', 'client_phone')
        }),
        ('Детали заказа', {
            'fields': ('service', 'shoot_date', 'total_amount', 'status')
        }),
        ('Дополнительно', {
            'fields': ('notes', 'order_date')
        }),
    )

# Расширенная регистрация Review с дополнительными возможностями
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройка отображения отзывов в админ-панели"""
    
    # Какие поля показывать в списке
    list_display = ['author_name', 'photo', 'rating', 'is_approved', 'created_at']
    
    # По каким полям можно фильтровать
    list_filter = ['is_approved', 'rating', 'created_at', 'photo']
    
    # По каким полям можно искать
    search_fields = ['author_name', 'text', 'email']
    
    # Какие поля можно редактировать прямо в списке
    list_editable = ['is_approved']
    
    # Поля только для чтения
    readonly_fields = ['created_at']
    
    # Сколько отзывов показывать на странице
    list_per_page = 20
# Register your models here.
