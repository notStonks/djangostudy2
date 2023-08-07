from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Product, ProductCategory, BasketItem
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView


class IndexView(TemplateView):
    template_name = "products/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store'
        return context


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = "Store - Каталог"
        context['categories'] = ProductCategory.objects.all()
        return context


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
