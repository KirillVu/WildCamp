from django.shortcuts import render
from apps.products.models import Product, Category

def home(request):
    products = Product.objects.filter(is_active=True).select_related("category").order_by("-created_at")[:8]
    categories = Category.objects.filter(is_active=True)[:8]
    return render(request, "core/home.html", {"products": products, "categories": categories})

def about(request):
    return render(request, "core/info.html", {"page_title": "О магазине", "page_text": "WILD CAMP — учебный интернет-магазин туристического снаряжения."})

def contacts(request):
    return render(request, "core/info.html", {"page_title": "Контакты", "page_text": "Демонстрационные контактные данные магазина WILD CAMP."})
