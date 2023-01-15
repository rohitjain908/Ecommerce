from django.shortcuts import render
from rest_framework import serializers
from .models import *
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Product
        fields = '__all__'



def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    products = Product.objects.all()
    responseProducts = ProductSerializer(products, many = True)
    userId = request.session['userId']
    user = User.objects.get(id = userId)
    if Cart.objects.filter(user = user, buy = False).exists():
        cart = Cart.objects.get(user = user, buy = False)
    else:
        cart = Cart.objects.create(user = user, buy = False)
        cart.save()

    total = cart.get_cart_items


    return render(request, 'dashboard.html', {'products': responseProducts.data, "total" : total})




def addItem(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == 'POST':
        productId = request.POST.get('productId')
        userId = request.session['userId']
        user = User.objects.get(id = userId)
        product = Product.objects.get(id = productId)

        

        if Cart.objects.filter(user = user, buy = False).exists():
            cart = Cart.objects.get(user = user, buy = False)
        else:
            cart = Cart.objects.create(user = user, buy = False)
            cart.save()
    

        if OrderProduct.objects.filter(product = product, cart = cart).exists():
            orderProduct = OrderProduct.objects.get(product = product, cart = cart)
            orderProduct.quantity = orderProduct.quantity + 1
            orderProduct.save()
        else:
            orderProduct = OrderProduct.objects.create(product = product, cart = cart, quantity = 1)
            orderProduct.save()

        

        total = 0
        totalOrderProducts = OrderProduct.objects.filter(cart = cart)
        for orderProduct in totalOrderProducts:
            total = total + orderProduct.quantity

        
        return JsonResponse({"status": 'Success', "total" : total, "price" : product.price}) 

    return JsonResponse({"status": 'Fail'}) 


def cart(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))


    userId = request.session['userId']
    user = User.objects.get(id = userId)

    if not Cart.objects.filter(user = user, buy = False):
        return render(request, 'cart.html', {"empty" : True})

    cart = Cart.objects.get(user = user, buy = False)
    orderProducts = OrderProduct.objects.filter(cart = cart)
    return render(request, 'cart.html', {"empty" : False, "products" : orderProducts, "cart" : cart})


def cartOrder(request):
    cartId = request.POST.get('cartId')
    Cart.objects.filter(id = cartId).update(buy = True)
    return JsonResponse({"status" : "Ordered"})


def add(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    orderProductId = request.POST.get('orderProductId')
    orderProduct = OrderProduct.objects.get(id = orderProductId)
    orderProduct.quantity = orderProduct.quantity + 1
    orderProduct.save()

    price = orderProduct.product.price

    return JsonResponse({"status": 'Success', "price" : price}) 


def remove(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    orderProductId = request.POST.get('orderProductId')
    orderProduct = OrderProduct.objects.get(id = orderProductId)
    orderProduct.quantity = orderProduct.quantity - 1
    orderProduct.save()
    price = orderProduct.product.price
    if orderProduct.quantity == 0:
        orderProduct.delete()
        return JsonResponse({"status": 'Success', "price" : price, "removed" : True}) 
    
    return JsonResponse({"status": 'Success', "price" : price, "removed" : False}) 
    
