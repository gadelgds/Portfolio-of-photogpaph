from django import forms
from .models import Review, Order

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

class OrderForm(forms.ModelForm):
    """Форма для создания заказа"""
    
    class Meta:
        model = Order
        fields = ['client_name', 'client_email', 'client_phone', 'shoot_date', 'notes']
        
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'client_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'shoot_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Дополнительные пожелания...',
                'rows': 4
            })
        }
        
        labels = {
            'client_name': 'Ваше имя',
            'client_email': 'Email',
            'client_phone': 'Телефон',
            'shoot_date': 'Желаемая дата съемки',
            'notes': 'Комментарий'
        }
