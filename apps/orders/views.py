from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.cart.models import Cart
from apps.products.models import Product
from .models import Order, OrderItem
from .forms import CheckoutForm

def _active_product(line):
    """Актуальная версия товара из корзины; если его скрыли или удалили, оформление прерывается с понятным сообщением."""
    try:
        return Product.objects.get(pk=line.product_id, is_active=True)
    except Product.DoesNotExist:
        raise ValueError(f"Товар «{line.product.name}» больше недоступен. Удалите его из корзины.")

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.error(request, "Корзина пуста.")
        return redirect("cart")
    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                cart_items = list(cart.items.select_related("product"))
                total = Decimal("0.00")
                for line in cart_items:
                    product = _active_product(line)
                    if line.quantity > product.stock:
                        raise ValueError(f"Недостаточно товара «{product.name}» на складе.")
                    total += product.price * line.quantity
                order = form.save(commit=False)
                order.user = request.user
                order.total_price = total
                order.save()
                for line in cart_items:
                    product = _active_product(line)
                    updated = Product.objects.filter(pk=product.pk, stock__gte=line.quantity).update(stock=models_f("stock") - line.quantity)
                    if not updated:
                        raise ValueError(f"Товар «{product.name}» уже закончился.")
                    OrderItem.objects.create(order=order, product=product, product_name=product.name, price=product.price, quantity=line.quantity)
                cart.items.all().delete()
            messages.success(request, f"Заказ №{order.pk} успешно оформлен.")
            return redirect("order_detail", pk=order.pk)
        except ValueError as exc:
            messages.error(request, str(exc))
    return render(request, "orders/checkout.html", {"form": form, "items": cart.items.select_related("product")})

from django.db.models import F as models_f

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/history.html", {"orders": orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=pk, user=request.user)
    return render(request, "orders/detail.html", {"order": order})
