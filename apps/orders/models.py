from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новый"
        CONFIRMED = "confirmed", "Подтверждён"
        PREPARING = "preparing", "Собирается"
        SHIPPED = "shipped", "Отправлен"
        DELIVERED = "delivered", "Доставлен"
        CANCELLED = "cancelled", "Отменён"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    full_name = models.CharField("ФИО", max_length=180)
    phone = models.CharField("Телефон", max_length=30)
    email = models.EmailField("Email")
    delivery_address = models.TextField("Адрес доставки")
    delivery_method = models.CharField("Способ доставки", max_length=80)
    payment_method = models.CharField("Способ оплаты", max_length=80)
    total_price = models.DecimalField("Итого", max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "заказ"
        verbose_name_plural = "Заказы"
    def __str__(self): return f"Заказ №{self.pk}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)
    product_name = models.CharField("Название на момент покупки", max_length=180)
    price = models.DecimalField("Цена на момент покупки", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", validators=[MinValueValidator(1)])
    def __str__(self): return self.product_name
