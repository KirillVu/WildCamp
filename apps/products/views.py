from decimal import Decimal, InvalidOperation

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Product, Category

PAGE_SIZE = 12
SORT_OPTIONS = [
    ("-created_at", "Сначала новые"),
    ("price", "Сначала дешевле"),
    ("-price", "Сначала дороже"),
    ("name", "По названию"),
]


def _to_decimal(value):
    """Возвращает Decimal или None, если введено не число."""
    try:
        return Decimal(value.replace(",", "."))
    except (InvalidOperation, AttributeError):
        return None


def _render_catalog(request, queryset, current_category=None):
    """Общая логика каталога и страницы категории: поиск, фильтры, сортировка, пагинация."""
    query = request.GET.get("q", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    available = request.GET.get("available", "")
    sort = request.GET.get("sort", "-created_at")
    category_id = request.GET.get("category", "")
    if current_category:
        category_id = str(current_category.pk)

    if query:
        queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if not current_category and category_id.isdigit():
        queryset = queryset.filter(category_id=int(category_id))
    if _to_decimal(min_price) is not None:
        queryset = queryset.filter(price__gte=_to_decimal(min_price))
    if _to_decimal(max_price) is not None:
        queryset = queryset.filter(price__lte=_to_decimal(max_price))
    if available == "1":
        queryset = queryset.filter(stock__gt=0)
    if sort not in dict(SORT_OPTIONS):
        sort = "-created_at"
    queryset = queryset.order_by(sort)

    paginator = Paginator(queryset, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))
    # None в списке означает многоточие «…» между номерами страниц
    page_range = [
        n if isinstance(n, int) else None
        for n in paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)
    ]
    return render(request, "products/catalog.html", {
        "page_obj": page_obj,
        "page_range": page_range,
        "categories": Category.objects.filter(is_active=True),
        "current_category": current_category,
        "query": query,
        "selected_category": category_id,
        "min_price": min_price,
        "max_price": max_price,
        "available": available,
        "sort": sort,
        "sort_options": SORT_OPTIONS,
        # панель фильтров на мобильных открыта, если какой-то фильтр уже применён
        "panel_open": bool(category_id or min_price or max_price or available == "1"),
    })


def catalog(request):
    return _render_catalog(request, Product.objects.filter(is_active=True).select_related("category"))


def category(request, slug):
    selected = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=selected, is_active=True).select_related("category")
    return _render_catalog(request, products, selected)


def product_detail(request, slug):
    item = get_object_or_404(Product, slug=slug, is_active=True)
    similar = Product.objects.filter(category=item.category, is_active=True).exclude(pk=item.pk)[:4]
    return render(request, "products/detail.html", {"product": item, "similar": similar})
