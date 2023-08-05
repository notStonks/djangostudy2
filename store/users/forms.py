from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите имя пользователя'
        }))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите пароль'
        }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(
        attrs={
            'class': 'form-control py-4', 'placeholder': 'Введите имя'
        }))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(
        attrs={
            'class': 'form-control py-4', 'placeholder': 'Введите фамилию'
        }))
    username = forms.CharField(label='Никнейм', widget=forms.TextInput(
        attrs={
            'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'
        }))
    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput(
        attrs={
            'class': 'form-control py-4', 'placeholder': 'Введите email'
        }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control py-4', 'placeholder': 'Введите пароль'
        }))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'
        }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(
        attrs={'class': 'form-control py-4'}
    ))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(
        attrs={'class': 'form-control py-4'}
    ))
    image = forms.ImageField(label="Изображение", widget=forms.FileInput(
        attrs={'class': 'custom-file-input'}
    ), required=False)
    username = forms.CharField(label="ник", widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'readonly': True}
    ))
    email = forms.CharField(label="email", widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'readonly': True}
    ))


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')
