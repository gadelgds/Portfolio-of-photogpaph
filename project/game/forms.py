from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Review, Order

class RegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    phone = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Телефон (необязательно)'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            })
        }
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'phone': 'Телефон',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        
        # Полностью убираем все валидаторы пароля
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []
    
    def _post_clean(self):
        """Переопределяем метод, чтобы пропустить валидацию паролей Django"""
        super(forms.ModelForm, self)._post_clean()
        # Проверяем только совпадение паролей
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают')

class LoginForm(AuthenticationForm):
    """Форма входа"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }), label='Имя пользователя')
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }), label='Пароль')

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
