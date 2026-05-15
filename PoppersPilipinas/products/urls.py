from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('<int:product_id>/buy-now/', views.buy_now, name='buy_now'),
    path('<int:product_id>/remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('sale/', views.sale, name='sale'),
]