from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = "Store - Авторизация"

    def get_success_url(self):
        return reverse_lazy("products:index")


class UserRegistrationView(SuccessMessageMixin, TitleMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy('users:login')
    success_message = "Вы успешно зарегистрированы"
    title = "Store - Регистрация"


class UserProfileView(LoginRequiredMixin, TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy('users:profile')
    title = "Store - Личный кабинет"

    def get_object(self, queryset=None):
        return self.request.user


class EmailVerificationView(TitleMixin, TemplateView):
    title = "Store - Подтверждение электронной почты"
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('products:index'))
