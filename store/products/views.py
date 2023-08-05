from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Product, ProductCategory, BasketItem


def index(request):
    context = {
        'title': 'Store',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Store - Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'products/products.html', context)


@login_required
def item_add(request, product_id):
    product = Product.objects.get(id=product_id)
    item = BasketItem.objects.get_or_create(user=request.user, product=product)[0]
    item.quantity += 1
    item.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def item_remove(request, basket_id):
    item = BasketItem.objects.get(id=basket_id)
    item.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])