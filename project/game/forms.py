from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """Форма для создания отзыва"""
    
    class Meta:
        model = Review
        # Какие поля показывать в форме (is_approved не показываем)
        fields = ['author_name', 'email', 'rating', 'text']
        
        # Настройка виджетов (как будут выглядеть поля)
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email (необязательно)'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите ваш отзыв...',
                'rows': 5
            })
        }
        
        # Русские названия полей
        labels = {
            'author_name': 'Ваше имя',
            'email': 'Email',
            'rating': 'Оценка',
            'text': 'Отзыв'
        }
