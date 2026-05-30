from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, verbose_name="Товар")
    text = models.TextField('Текст отзыва')
    rating = models.IntegerField('Оценка', default=5)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'