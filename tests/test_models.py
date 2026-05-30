import pytest
from decimal import Decimal
from django.contrib.auth.models import User

from catalog.models import Category, Product
from orders.models import Order, OrderItem
from reviews.models import Review
from users.models import Profile

@pytest.fixture
def category(db):
    return Category.objects.create(name="Смартфоны", slug="smartphones")

@pytest.fixture
def product(db, category):
    return Product.objects.create(
        category=category,
        title="iPhone 15",
        description="Крутой телефон",
        price=Decimal("99999.99"),
        is_available=True,
    )

@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="pass123")

@pytest.fixture
def order(db, user):
    return Order.objects.create(user=user)

@pytest.mark.django_db
class TestCategory:
    def test_str(self, category):
        """Category.__str__ должен возвращать название категории"""
        assert str(category) == "Смартфоны"

@pytest.mark.django_db
class TestOrderItem:
    def test_price_snapshot(self, order, product):
        """Цена в OrderItem должна сохраняться как снимок на момент заказа и не меняться, если потом изменилась цена самого товара"""
        item = OrderItem.objects.create(
            order=order,
            product=product,
            price=Decimal("12345.00"),
            quantity=1,
        )
        product.price = Decimal("1.00")
        product.save()
        item.refresh_from_db()
        assert item.price == Decimal("12345.00")

@pytest.mark.django_db
class TestProfileSignals:
    def test_auto_created_on_user_create(self):
        """При создании User должен автоматически создаваться Profile"""
        new_user = User.objects.create_user(username="bob", password="pass")
        assert Profile.objects.filter(user=new_user).exists()

@pytest.mark.django_db
class TestProduct:
    def test_product_availability_default(self, category):
        """Проверка, что новый товар по умолчанию создается доступным, если не указано иное"""
        new_product = Product.objects.create(
            category=category,
            title="Чехол",
            description="Просто чехол",
            price=Decimal("1000.00")
        )
        assert new_product.is_available is True

@pytest.mark.django_db
class TestReview:
    def test_review_creation_and_relations(self, user, product):
        """Проверка корректного создания отзыва и его связей с юзером и товаром"""
        review = Review.objects.create(
            product=product,
            user=user,
            text="Отличный товар!",
            rating=5
        )
        assert review.product.title == "iPhone 15"
        assert review.user.username == "alice"
        assert review.rating == 5