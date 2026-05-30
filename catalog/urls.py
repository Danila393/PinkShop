from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_list_view, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('products/<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
]