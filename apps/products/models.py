from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField("Название", max_length=120, unique=True)
    slug = models.SlugField("URL", max_length=140, unique=True, blank=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="Категория")
    name = models.CharField("Название", max_length=180)
    slug = models.SlugField("URL", max_length=200, unique=True, blank=True)
    short_description = models.CharField("Краткое описание", max_length=255, blank=True)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена, ₽", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField("Остаток", default=0)
    image = models.ImageField("Изображение", upload_to="products/", blank=True, null=True)
    specifications = models.JSONField("Характеристики", default=dict, blank=True)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Добавлен", auto_now_add=True)
    updated_at = models.DateTimeField("Изменён", auto_now=True)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]
        constraints = [models.CheckConstraint(condition=models.Q(price__gte=0), name="product_price_nonnegative")]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery", verbose_name="Товар")
    image = models.ImageField("Фотография", upload_to="products/gallery/")
    alt_text = models.CharField("Alt-текст", max_length=180, blank=True)

    class Meta:
        verbose_name = "фотография товара"
        verbose_name_plural = "Фотографии товаров"

    def __str__(self):
        return f"Фото: {self.product.name}"
