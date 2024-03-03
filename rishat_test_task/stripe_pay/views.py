import json
import random

import stripe
from django.conf import settings
from django.http import (HttpResponseBadRequest, HttpResponseServerError,
                         JsonResponse)
from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_http_methods

from .models import Discount, Item, Order, Tax

stripe.api_key = settings.STRIPE_SECRET_KEY


class IndexView(View):
    """Рендерит главную страницу со всеми продуктами"""

    def get(self, request):
        items = Item.objects.all()
        first_item = items.first()
        context = {
            'items': items,
            'currency': self.get_currency_symbol(first_item.currency),
        }
        return render(request, 'index.html', context)

    def get_currency_symbol(self, currency):
        currencies = {
            "eur": "€",
            "usd": "$",
        }
        return currencies[currency]


class CreateOrderView(View):
    """Создает заказ и сессию Stripe"""

    def post(self, request):
        try:
            items_ids = json.loads(request.body).get('idList')
            items_ids = set(map(int, items_ids))
            new_order = Order.objects.create(has_discount=bool(random.getrandbits(1)))
            new_order.items.add(*items_ids)
            if new_order.has_discount:
                discount_amount = random.randint(1, 90)
                discount = Discount.objects.get_or_create(amount=discount_amount)
                new_order.discounts.add(discount[0])
                stripe_discount = stripe.Coupon.create(
                    percent_off=discount[0].amount,
                    duration="once",
                )
            new_order.save()
            tax_amount = random.randint(10, 25)
            tax = Tax.objects.get_or_create(amount=tax_amount)
            new_order.taxes.add(tax[0])
            stripe_tax = stripe.TaxRate.create(
                display_name="VAT",
                inclusive=True,
                percentage=tax[0].amount,
            )
            items = Item.objects.filter(id__in=items_ids)
            line_items = []
            for item in items:
                print(item.currency)
                line_item = {
                    "price_data": {
                        "currency": item.currency,
                        "product_data": {
                            "name": item.name
                        },
                        "unit_amount": int(item.price * 100),
                    },
                    "tax_rates": [f'{stripe_tax.id}'],
                    "quantity": 1
                }
                line_items.append(line_item)
            session_params = {
                "payment_method_types": ['card'],
                "line_items": line_items,
                "mode": 'payment',
                # Пришлось захардкодить, поскольку иначе использовалось имя контейнера и редирект ломался
                "success_url": 'http://' + settings.HOST + '/success/',
                "cancel_url": 'http://' + settings.HOST + '/cancel/',
            }
            if new_order.has_discount:
                session_params["discounts"] = [{"coupon": f'{stripe_discount.id}'}]
            session = stripe.checkout.Session.create(**session_params)
            return JsonResponse({'session_id': session.id, 'publishable_key': settings.STRIPE_PUBLISHABLE_KEY})
        except stripe.error.StripeError as e:
            return HttpResponseBadRequest(f'Stripe unable to proceed with payment due to: {e}')
        except Exception as e:
            return HttpResponseServerError(f'Some server error occured: {e}')


@require_http_methods(["GET"])
def success_view(request):
    """Отдает страницу успешного платежа"""
    return render(request, 'success.html')


@require_http_methods(["GET"])
def cancel_view(request):
    """Отдает страницу отмены платежа"""
    return render(request, 'cancel.html')
