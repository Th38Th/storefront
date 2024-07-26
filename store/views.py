from django.http import HttpRequest
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
import django.core.serializers as serializers
from django.db.models import Q
from .models import Product
from .models import CartItem
from .models import User
from .models import Cart
import time

def ensure_cart(request : HttpRequest):    
    userid = request.session["userid"] if "userid" in request.session else None
    if "cartid" not in request.session:
        try:
            user = User.objects.get(pk=userid)
        except:
            user = None
        cart = Cart.objects.create(user=user)
        cart.save()
        request.session["cartid"] = cart.pk
    else:
        cart, created = Cart.objects.get_or_create(pk=request.session["cartid"])
        if created:
            cart.save()
    return cart

# Create your views here.
def products_page(request):
    return render(request, "products.html")

def get_products(request):
    products = Product.objects.all()
    products_json = serializers.serialize('json',products)
    return JsonResponse({"json": products_json, "html": render_to_string("products_contents.html", {'products': products})})

def get_products_filtered(request : HttpRequest):
    products = Product.objects
    try:
        price_min = float(request.GET["price_min"])
        products = products.filter(price__gte=price_min)
    except:
        pass
    try:
        price_max = float(request.GET["price_max"])
        products = products.filter(price__lte=price_max)
    except:
        pass
    try:
        sort_on = request.GET["sort_on"]
        sort_order = request.GET["sort_order"]
        sort_on = "-"+sort_on if sort_order == 'DESC' else sort_on
        products = products.order_by(sort_on)
    except:
        pass
    try:
        text_has = request.GET["text_has"]
        products = products.filter(Q(title__icontains=text_has) | Q(description__icontains=text_has)) 
    except:
        pass
    time.sleep(.25)
    products_json = serializers.serialize('json',products)
    return JsonResponse({"json": products_json, "html": render_to_string("products_contents.html", {'products': products})})

def get_cart_contents(request : HttpRequest):
    cart = ensure_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        item.value = item.product.price * item.quantity
    items_json = serializers.serialize('json',cart_items)
    return JsonResponse({"json": items_json, "sum": sum(map(lambda item: item.value, cart_items)),
                         "html": render_to_string("cart_contents.html", {'cart_items': cart_items})})

def add_cart_item(request : HttpRequest):
    cart = ensure_cart(request)
    qty = int(request.POST["qty"])
    productId = request.POST["id"]
    prod = Product.objects.get(pk=productId)
    item, _ = CartItem.objects.get_or_create(cart=cart, product=prod)
    item.quantity = qty
    item.save()
    return JsonResponse({'success': True, 'message': 'Product added to cart', 'quantity': item.quantity})

def get_cart_item(request : HttpRequest):
    cart = ensure_cart(request)
    productId = request.GET["id"]
    try:
        prod = Product.objects.get(pk=productId)
        item = CartItem.objects.get(cart=cart, product=prod)
        qty = item.quantity
    except:
        qty = 0
    return JsonResponse({'quantity': qty})

def merge_cart_item(request: HttpRequest):
    cart = ensure_cart(request)
    qty = int(request.POST["qty"])
    productId = request.POST["id"]
    prod = Product.objects.get(pk=productId)
    try:
        item, _ = CartItem.objects.get_or_create(cart=cart, product=prod)
        item.quantity = min(qty, prod.stock)
        if item.quantity <= 0:
            message = 'Product removed from cart'
            item.delete()
        else:
            message = 'Product updated in cart'
            item.save()
        success = True
    except Exception as e:
        message = "Could not update product in cart"
        success = False
    return JsonResponse({'success': success, 'message': message, 'quantity': qty})

def checkout(request: HttpRequest):
    cart = ensure_cart(request)
    items = CartItem.objects.filter(cart=cart)
    total = sum(map(lambda item: item.product.price * item.quantity, items))
    del request.session["cartid"]
    message = 'Successfully checked out!'
    return JsonResponse({'message': message, 'total': total})

def about_page(request: HttpRequest):
    return render(request, "about.html")

def home_page(request: HttpRequest):
    return render(request, "home.html")

def contact_page(request: HttpRequest):
    return render(request, "contact.html")