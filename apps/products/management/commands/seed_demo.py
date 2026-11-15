from decimal import Decimal

from django.core.management.base import BaseCommand
from apps.products.models import Category, Product


class Command(BaseCommand):
    help = "Добавляет демонстрационные категории и товары WILD CAMP"

    def handle(self, *args, **options):
        catalog = [
            {
                "category": "Палатки и тенты",
                "category_description": "Укрытия для ночёвок, кемпинга и походов.",
                "products": [
                    {
                        "name": "Палатка Trek 2",
                        "slug": "palatka-trek-2",
                        "short_description": "Двухместная палатка для походов и кемпинга.",
                        "description": "Лёгкая двухместная палатка с тамбуром для хранения обуви и рюкзаков. Подходит для туристических маршрутов и отдыха на природе.",
                        "price": Decimal("8490.00"), "stock": 12,
                        "specifications": {"Вместимость": "2 человека", "Сезонность": "3 сезона", "Вес": "2,4 кг", "Материал": "Полиэстер"},
                    },
                    {
                        "name": "Тент защитный 3×3 м",
                        "slug": "tent-protect-3x3",
                        "short_description": "Универсальный тент от солнца и дождя.",
                        "description": "Прочный универсальный тент для организации навеса над лагерем, зоной отдыха или снаряжением.",
                        "price": Decimal("3290.00"), "stock": 20,
                        "specifications": {"Размер": "3×3 м", "Материал": "Оксфорд", "Водостойкость": "3000 мм", "Цвет": "Оливковый"},
                    },
                ],
            },
            {
                "category": "Спальные мешки",
                "category_description": "Спальные мешки и аксессуары для комфортного сна.",
                "products": [
                    {
                        "name": "Спальный мешок North -5",
                        "slug": "sleeping-bag-north-5",
                        "short_description": "Тёплый спальник-кокон для прохладных ночей.",
                        "description": "Спальный мешок-кокон с капюшоном и удобной молнией. Рассчитан на использование в прохладную погоду.",
                        "price": Decimal("4590.00"), "stock": 15,
                        "specifications": {"Форма": "Кокон", "Температура комфорта": "+2 °C", "Предельная температура": "−5 °C", "Вес": "1,5 кг"},
                    },
                ],
            },
            {
                "category": "Рюкзаки и сумки",
                "category_description": "Рюкзаки для коротких прогулок и многодневных маршрутов.",
                "products": [
                    {
                        "name": "Туристический рюкзак Ranger 45",
                        "slug": "backpack-ranger-45",
                        "short_description": "Вместительный рюкзак с регулируемой спинкой.",
                        "description": "Рюкзак объёмом 45 литров с поясным ремнём, боковыми карманами и регулируемой подвесной системой.",
                        "price": Decimal("6790.00"), "stock": 9,
                        "specifications": {"Объём": "45 л", "Материал": "Полиэстер 600D", "Вес": "1,3 кг", "Цвет": "Тёмно-зелёный"},
                    },
                ],
            },
            {
                "category": "Посуда и приготовление",
                "category_description": "Всё необходимое для приготовления еды на природе.",
                "products": [
                    {
                        "name": "Набор походной посуды CampCook",
                        "slug": "campcook-cookware-set",
                        "short_description": "Компактный набор посуды для двух туристов.",
                        "description": "Набор из котелка, сковороды и двух кружек. Предметы компактно складываются друг в друга для экономии места.",
                        "price": Decimal("2190.00"), "stock": 24,
                        "specifications": {"Количество предметов": "4", "Материал": "Анодированный алюминий", "Вместимость котелка": "1,5 л", "Вес": "620 г"},
                    },
                ],
            },
            {
                "category": "Освещение и инструменты",
                "category_description": "Фонари и полезные инструменты для лагеря.",
                "products": [
                    {
                        "name": "Фонарь кемпинговый Glow 500",
                        "slug": "camping-lantern-glow-500",
                        "short_description": "Компактный фонарь с несколькими режимами света.",
                        "description": "Перезаряжаемый кемпинговый фонарь для освещения палатки и лагеря. Яркость регулируется в нескольких режимах.",
                        "price": Decimal("1890.00"), "stock": 30,
                        "specifications": {"Яркость": "До 500 лм", "Питание": "USB-C аккумулятор", "Режимы": "3", "Вес": "280 г"},
                    },
                    {
                        "name": "Мультитул Trail 11",
                        "slug": "multitool-trail-11",
                        "short_description": "Компактный мультитул для бытовых задач в походе.",
                        "description": "Многофункциональный инструмент для несложных ремонтных и хозяйственных задач в лагере. Оснащён чехлом для хранения.",
                        "price": Decimal("2490.00"), "stock": 18,
                        "specifications": {"Количество функций": "11", "Материал корпуса": "Нержавеющая сталь", "Комплектация": "Мультитул, чехол", "Вес": "240 г"},
                    },
                ],
            },
        ]

        created_categories = 0
        created_products = 0
        for entry in catalog:
            category, category_created = Category.objects.update_or_create(
                name=entry["category"],
                defaults={"description": entry["category_description"], "is_active": True},
            )
            created_categories += int(category_created)
            for item in entry["products"]:
                _, product_created = Product.objects.update_or_create(
                    slug=item["slug"],
                    defaults={**item, "category": category, "is_active": True},
                )
                created_products += int(product_created)

        self.stdout.write(self.style.SUCCESS(
            f"Готово! Категорий: {Category.objects.count()}, товаров: {Product.objects.count()}. "
            f"Добавлено новых: категорий — {created_categories}, товаров — {created_products}."
        ))
