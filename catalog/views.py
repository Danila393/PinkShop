from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from reviews.models import Review
from reviews.forms import ReviewForm


def home_view(request):
    return render(request, 'catalog/home.html')


def product_list_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    form = ReviewForm()

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    p_id = str(product_id)

    if p_id in cart:
        cart[p_id] += 1
    else:
        cart[p_id] = 1

    request.session['cart'] = cart
    return redirect('catalog:cart_view')


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total_price = 0

    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        line_total = product.price * qty
        total_price += line_total
        items.append({
            'product': product,
            'qty': qty,
            'line_total': line_total
        })

    return render(request, 'catalog/cart.html', {
        'items': items,
        'total_price': total_price
    })


def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('catalog:cart_view')


def toggle_theme(request):
    current_theme = request.COOKIES.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'


    response = redirect(request.META.get('HTTP_REFERER', 'catalog:home'))
    response.set_cookie('theme', new_theme, max_age=365 * 24 * 60 * 60)
    return response


def chat_room(request, room_name):
    return render(request, 'catalog/chat.html', {
        'room_name': room_name
    })