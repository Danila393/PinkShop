from rest_framework import generics
from drf_spectacular.utils import extend_schema
from django.contrib.auth.models import User
from catalog.models import Category, Product
from reviews.models import Review
from orders.models import Order

from .serializers import (
    CategorySerializer, ProductSerializer, ReviewSerializer,
    OrderSerializer, UserShortSerializer
)

@extend_schema(summary="Список категорий", tags=["Категории"])
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@extend_schema(summary="Список товаров", tags=["Товары"])
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@extend_schema(summary="Детальная информация о товаре", tags=["Товары"])
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@extend_schema(summary="Список заказов", tags=["Заказы"])
class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@extend_schema(summary="Детальная информация о заказе", tags=["Заказы"])
class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@extend_schema(summary="Список отзывов", tags=["Отзывы"])
class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

@extend_schema(summary="Детальная информация об отзыве", tags=["Отзывы"])
class ReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

@extend_schema(summary="Профиль текущего пользователя", tags=["Пользователи"])
class CurrentUserAPIView(generics.RetrieveAPIView):
    serializer_class = UserShortSerializer

    def get_object(self):
        return self.request.user