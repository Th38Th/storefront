from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_page),
    path('home/', views.home_page),
    path('about/', views.about_page),
    path('contact/', views.contact_page),
    path('products/', views.products_page),
    path('get-products/', views.get_products),
    path('get-products-filtered', views.get_products_filtered),
    path('cart/', views.get_cart_contents),
    path('checkout/', views.checkout),
    path('add-cart-item/', views.add_cart_item),
    path('update-cart-item/', views.update_cart_item),
    path('get-cart-item', views.get_cart_item)
]