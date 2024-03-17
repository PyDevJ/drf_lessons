import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(name, description):
    """Создание продукта в Stripe."""
    product = stripe.Product.create(
        name=name,
        description=description
    )
    return product.id


def create_price(product_id, price_amount, currency):
    """Создание цены в Stripe."""
    if price_amount is not None:
        price_amount = int(price_amount) * 100  # Цены в Stripe указываются в копейках
        price = stripe.Price.create(
            product=product_id,
            unit_amount=price_amount,
            currency=currency
        )
        return price.id
    else:
        return None


def create_checkout_session(price_id, success_url, cancel_url):
    """Создание сессии для платежа в Stripe."""
    session = stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1
            }
        ],
        mode="payment"
    )
    return session.url
