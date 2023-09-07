from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import BasketItem

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    title = "Store - Оформление заказа"
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        basket = BasketItem.objects.filter(user=self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=basket.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:cancel')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.buyer = self.request.user
        return super(OrderCreateView, self).form_valid(form)


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CancelTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/cancel.html'
    title = 'Store - Отмена заказа'


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = ('-created',)

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(buyer=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Заказ № {self.object.id}'
        return context


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    print(request)
    print()
    print(payload)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        fulfill_order(session.metadata)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(metadata):
    order_id = int(metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
