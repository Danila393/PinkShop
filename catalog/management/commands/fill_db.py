from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalog.models import Category, Product
from orders.models import Order, OrderItem
from reviews.models import Review
import random


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def _create_users(self):
        users = []
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
            self.stdout.write("Создали суперюзера admin")

        for i in range(1, 4):
            user, created = User.objects.get_or_create(
                username=f"user{i}",
                defaults={"email": f"user{i}@mail.com"}
            )
            if created:
                user.set_password("qwerty123")
                user.save()
                self.stdout.write(f"Создали юзера {user.username}")
            users.append(user)
        return users

    def _create_categories(self):
        names = ["Сумки", "Одежда", "Обувь"]
        categories = []
        for name in names:
            cat, _ = Category.objects.get_or_create(name=name)
            categories.append(cat)
        self.stdout.write("Создали категории")
        return categories

    def _create_products(self, categories):
        titles = ["Розовый рюкзак", "Кроссовки розовые", "Майка розовая"]
        products = []
        for i in range(10):
            cat = random.choice(categories)
            prod, _ = Product.objects.get_or_create(
                title=f"{random.choice(titles)} {i + 1}",
                defaults={
                    "category": cat,
                    "description": "Супер пупер классный товар!",
                    "price": random.randint(1000, 5000),
                    "is_available": True
                }
            )
            products.append(prod)
        self.stdout.write("Создали товары")
        return products

    def _create_orders(self, users, products):
        for i in range(5):
            user = random.choice(users)
            order = Order.objects.create(user=user)
            OrderItem.objects.create(
                order=order,
                product=random.choice(products),
                price=random.randint(1000, 5000),
                quantity=1
            )
        self.stdout.write("Создали заказы")

    def _create_reviews(self, users, products):
        for i in range(5):
            user = random.choice(users)
            Review.objects.get_or_create(
                user=user,
                product=random.choice(products),
                defaults={"text": "Всё супер!", "rating": 5}
            )
        self.stdout.write("Отзывы тоже создали")

    def handle(self, *args, **options):
        users = self._create_users()
        categories = self._create_categories()
        products = self._create_products(categories)
        self._create_orders(users, products)
        self._create_reviews(users, products)
        self.stdout.write(self.style.SUCCESS("УРА БД ЗАПОЛНЕНА"))