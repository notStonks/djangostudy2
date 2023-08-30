from products.models import BasketItem


def basket(request):
    """
    Можно также использовать Related objects в шаблонах
    (user.basketitem_set.all или user.basketitem_set.all.total_quantity)
    """

    user = request.user
    return {"basket": BasketItem.objects.filter(user=user) if user.is_authenticated else []}
