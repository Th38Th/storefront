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
    path('merge-cart-item/', views.merge_cart_item)
]