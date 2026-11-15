from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.products.models import Product
from .models import Cart, CartItem

@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("product")
    total = sum((item.subtotal for item in items), start=0)
    return render(request, "cart/cart.html", {"cart": cart, "items": items, "total": total})

@login_required
def add_to_cart(request, product_id):
    if request.method != "POST": return redirect("catalog")
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    if product.stock < 1:
        messages.error(request, "Товар закончился.")
        return redirect("product_detail", slug=product.slug)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": 1})
    if not created and item.quantity < product.stock:
        item.quantity += 1
        item.save(update_fields=["quantity"])
    messages.success(request, "Товар добавлен в корзину.")
    return redirect("cart")

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    if request.method == "POST":
        try: quantity = int(request.POST.get("quantity", 1))
        except ValueError: quantity = 1
        if quantity < 1: item.delete()
        elif quantity <= item.product.stock:
            item.quantity = quantity
            item.save(update_fields=["quantity"])
        else: messages.error(request, "Недостаточно товара на складе.")
    return redirect("cart")

@login_required
def remove_from_cart(request, item_id):
    if request.method == "POST":
        get_object_or_404(CartItem, pk=item_id, cart__user=request.user).delete()
    return redirect("cart")
