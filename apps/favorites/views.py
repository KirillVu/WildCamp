from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.products.models import Product
from .models import Favorite

@login_required
def favorites(request):
    items = Favorite.objects.filter(user=request.user).select_related("product")
    return render(request, "favorites/list.html", {"items": items})

@login_required
def toggle_favorite(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        obj, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created: obj.delete()
    return redirect(request.META.get("HTTP_REFERER", "catalog"))
