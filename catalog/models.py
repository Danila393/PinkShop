from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_length=10, max_digits=10, decimal_places=2, verbose_name="Цена")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    image_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="Путь к картинке")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title

class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255, verbose_name="Комната")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    message = models.TextField(verbose_name="Сообщение")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чата"

    def __str__(self):
        username = self.user.username if self.user else "Аноним"
        return f"[{self.timestamp.strftime('%H:%M')}] {username}: {self.message}"