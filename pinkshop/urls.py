from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from . import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('catalog.urls', namespace='catalog')),
    path('users/', include('users.urls', namespace='users')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('orders/', include('orders.urls', namespace='orders')),

    path('api/categories/', api_views.CategoryListAPIView.as_view(), name='api_categories'),
    path('api/products/', api_views.ProductListAPIView.as_view(), name='api_products'),
    path('api/products/<int:pk>/', api_views.ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('api/reviews/', api_views.ReviewListAPIView.as_view(), name='api_reviews'),
    path('api/reviews/<int:pk>/', api_views.ReviewDetailAPIView.as_view(), name='api_review_detail'),
    path('api/orders/', api_views.OrderListAPIView.as_view(), name='api_orders'),
    path('api/orders/<int:pk>/', api_views.OrderDetailAPIView.as_view(), name='api_order_detail'),
    path('api/users/me/', api_views.CurrentUserAPIView.as_view(), name='api_me'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)