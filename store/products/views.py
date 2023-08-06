from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Product, ProductCategory, BasketItem
from django.core.paginator import Paginator


def index(request):
    context = {
        'title': 'Store',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    products = Product.objects.filter(category=category_id) if category_id else Product.objects.all()
    per_page = 3
    page_number = request.GET.get('page_number', 1)
    if not isinstance(page_number, int):
        if page_number.isdigit():
            page_number = int(page_number)
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)
    context = {
        'title': 'Store - Каталог',
        'products': products_paginator,
        'categories': ProductCategory.objects.all(),
        'category_id': category_id
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
