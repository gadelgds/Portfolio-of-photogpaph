from django.contrib import admin
from .models import Photo, Service, Review

# Расширенная регистрация Photo
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Настройка отображения фотографий в админ-панели"""
    list_display = ['title', 'likes', 'views', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['title']
    readonly_fields = ['likes', 'views', 'uploaded_at']

# Регистрация Service
admin.site.register(Service)

# Расширенная регистрация Review с дополнительными возможностями
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройка отображения отзывов в админ-панели"""
    
    # Какие поля показывать в списке
    list_display = ['author_name', 'rating', 'is_approved', 'created_at']
    
    # По каким полям можно фильтровать
    list_filter = ['is_approved', 'rating', 'created_at']
    
    # По каким полям можно искать
    search_fields = ['author_name', 'text', 'email']
    
    # Какие поля можно редактировать прямо в списке
    list_editable = ['is_approved']
    
    # Поля только для чтения
    readonly_fields = ['created_at']
    
    # Сколько отзывов показывать на странице
    list_per_page = 20
# Register your models here.
