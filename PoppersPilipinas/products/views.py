from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from .models import Product

SESSION_CART_KEY = 'cart'


def _get_cart(request):
    return request.session.get(SESSION_CART_KEY, {})


def _save_cart(request, cart):
    request.session[SESSION_CART_KEY] = cart
    request.session.modified = True


def _cart_item_count(request):
    return sum(_get_cart(request).values())


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {
        'products': products,
        'cart_item_count': _cart_item_count(request),
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {
        'product': product,
        'cart_item_count': _cart_item_count(request),
    })


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        cart = _get_cart(request)
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        _save_cart(request, cart)
        message = f'"{product.prodname}" added to cart.'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': message,
                'cart_item_count': _cart_item_count(request),
            })
        messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def buy_now(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        cart = _get_cart(request)
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        _save_cart(request, cart)
        messages.success(request, f'"{product.prodname}" added to cart. Proceed to checkout.')
        return redirect('products:cart')
    return redirect('/')


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = _get_cart(request)
        if str(product_id) in cart:
            product = get_object_or_404(Product, pk=product_id)
            cart.pop(str(product_id), None)
            _save_cart(request, cart)
            messages.success(request, f'"{product.prodname}" removed from cart.')
    return redirect('products:cart')


def cart_view(request):
    cart = _get_cart(request)
    product_ids = [int(pk) for pk in cart.keys()]
    products = Product.objects.filter(pk__in=product_ids)
    cart_items = []
    total_price = Decimal('0.00')

    for product in products:
        quantity = cart.get(str(product.id), 0)
        line_total = product.price * quantity
        total_price += line_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'line_total': line_total,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_item_count': _cart_item_count(request),
    })


def checkout(request):
    if request.method == 'POST':
        request.session[SESSION_CART_KEY] = {}
        request.session.modified = True
        messages.success(request, 'Checkout complete. Your cart has been cleared.')
        return redirect('products:index')
    return redirect('products:cart')


def sale(request):
    return HttpResponse("Sale Items here...")