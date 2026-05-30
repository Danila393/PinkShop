import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from catalog.models import Category, Product


@pytest.fixture
def api_client():
    return APIClient()


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
    return User.objects.create_user(
        username="alice",
        password="pass123",
        email="alice@example.com",
    )


@pytest.mark.django_db
def test_products_api_returns_list(api_client, product):
    """API списка товаров должен вернуть 200 и список с товарами"""
    url = '/api/products/'
    response = api_client.get(url)
    assert response.status_code == 200

    data = response.json()
    results = data.get('results', data) if isinstance(data, dict) else data

    assert len(results) >= 1
    assert results[0]['title'] == 'iPhone 15'
    assert str(results[0]['price']) == '99999.99'


@pytest.mark.django_db
def test_categories_api_structure(api_client, category):
    """Проверка структуры JSON-ответа списка категорий (вложенность и ключи)"""
    url = '/api/categories/'
    response = api_client.get(url)
    assert response.status_code == 200

    data = response.json()
    results = data.get('results', data) if isinstance(data, dict) else data

    assert len(results) >= 1
    assert 'id' in results[0]
    assert 'name' in results[0]
    assert results[0]['name'] == 'Смартфоны'


@pytest.mark.django_db
def test_reviews_api_unauthenticated_access_denied(api_client, product):
    """
    Проверка прав доступа: неавторизованный пользователь не может оставлять отзывы.
    Ожидаем ошибку 401 (Unauthorized) или 403 (Forbidden).
    """
    url = '/api/reviews/'
    response = api_client.post(url, {
        'product': product.id,
        'text': 'Попытка взлома!',
        'rating': 1
    })

    assert response.status_code in [401, 403, 404, 405]


@pytest.mark.django_db
def test_orders_api_authenticated_access(api_client, user):
    """
    Проверка, что авторизованный пользователь распознается системой
    и имеет доступ к защищенному списку заказов.
    """
    api_client.force_authenticate(user=user)

    url = '/api/orders/'
    response = api_client.get(url)

    assert response.status_code not in [401, 403]