from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import BasketItem

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('products:index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Поздравляю с успешной регистрацией")
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    if request.POST:
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    basket = BasketItem.objects.filter(user=request.user)
    total_sum = sum(item.sum() for item in basket)
    total_quantity = sum(item.quantity for item in basket)
    # total_sum, total_quantity = 0, 0
    # for item in basket:
    #     total_sum += item.sum()
    #     total_quantity += item.quantity

    context = {
        'title': 'Store - Профиль',
        'form': form,
        'basket': basket,
        'total_sum': total_sum,
        'total_quantity': total_quantity
    }
    return render(request, 'users/profile.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:index'))
