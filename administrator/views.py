from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from files.models import Image
from orders.models import Order, OrderProduct
from products.models import Product, ProductImage
from .models import User, Token
from rest_framework import status
from django.conf import settings
from orders.serializers import getOrder
from products.serializers import getProduct
from django.shortcuts import get_object_or_404
from functools import wraps
from django.contrib.auth.hashers import make_password, verify_password



def isAdmin(view_func):
    @wraps(view_func)
    def decorator(request, *args, **kwargs):
        token = request.headers.get("Admin-Authorization")
        if not token or token == 'unauthorized':
            return JsonResponse({'error': 'User ID not found in headers.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            t = Token.objects.get(token=token)
        except :
            return JsonResponse({'error': 'Unauthorized.'}, status=status.HTTP_404_NOT_FOUND)
        return view_func(request, *args, **kwargs)
    return decorator


@csrf_exempt
def authentificate(request):
    data = JSONParser().parse(request)
    user = User.objects.filter(username = data["username"])
    res = {
        "init": True,
        "logged": False,
    }
    if (not user.exists()): return JsonResponse(res, status = status.HTTP_403_FORBIDDEN, safe=False)
    user = user[0]
    if (verify_password(data["password"], user.password)[0]):
        token = Token.objects.create(user = user)        
        token.save()
        res = {
            "init": True,
            "logged": True,
            "token": token.token
        }
        return JsonResponse(res, status = status.HTTP_200_OK, safe=False)
    return JsonResponse(res, status = status.HTTP_403_FORBIDDEN, safe=False)
    

def authorization(request, token):
    try:
        token = Token.objects.get(token = token)
    except:
        res = { 
            "init": True,
            "logged": False 
        }
        return JsonResponse(res, safe=False)
    res = { 
        "init": True,
        "logged": True 
    }
    return JsonResponse(res, safe=False)


@csrf_exempt
def register(request):
    data = JSONParser().parse(request)
    user = User.objects.create(
        username = data["username"],
        password = make_password(data["password"])
    )
    user.save()
    return JsonResponse({}, safe=False)


@isAdmin
def getProducts(request, index):
    products = Product.objects.order_by("-date")
    res = {
        "products": [],
        "more": (products.count() - 10 * (index - 1)) >= 10
    }
    for product in products[10 * (index - 1): 10 * index]:
        res["products"].append(getProduct(product))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@isAdmin
def getProductById(request, id):
    product = get_object_or_404(Product, id = id)
    res = getProduct(product)
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
@isAdmin
def createProduct(request):
    data = JSONParser().parse(request)
    product = Product.objects.create(
        name = data["name"],
        description = data["description"],
        price = data["price"]
    )
    product.save()
    for image in data["images"]:
        productImage = ProductImage.objects.create(
            product = product,
            image = Image.objects.get(id = image["id"]),
            main = image["main"]
        )
        productImage.save()
    res = getProduct(product)
    return JsonResponse(res, status=status.HTTP_201_CREATED)


@isAdmin
@csrf_exempt
def updateProduct(request, id):
    data = JSONParser().parse(request)
    product = get_object_or_404(Product, id = id)
    product.name = data["name"]
    product.description = data["description"]
    product.price = data["price"]
    product.save()
    for productImage in ProductImage.objects.filter(product = product):
        productImage.delete()
    for image in data["images"]:
        productImage = ProductImage.objects.create(
            product = product,
            image = Image.objects.get(id = image["id"]),
            main = image["main"]
        )
        productImage.save()
    res = getProduct(product)
    return JsonResponse(res, status=status.HTTP_200_OK)


@isAdmin
@csrf_exempt
def deleteProduct(request, id):
    product = get_object_or_404(Product, id = id)
    res = getProduct(product)
    product.delete()
    return JsonResponse(res, status=status.HTTP_200_OK)


@isAdmin
def getOrders(request, index):
    orders = Order.objects.order_by("-date")
    res = {
        "orders": [],
        "more": (orders.count() - 10 * (index - 1)) >= 10
    }
    for order in orders[10 * (index - 1): 10 * index]:
        res["orders"].append(getOrder(order))
    return JsonResponse(res, status=status.HTTP_200_OK)


@isAdmin
def completeOrder(request, id):
    order = get_object_or_404(Order, id = id)
    order.completed = True
    res = getOrder(order)
    order.save()
    return JsonResponse(res, status=status.HTTP_200_OK)


@isAdmin
@csrf_exempt
def deleteOrder(request, id):
    order = get_object_or_404(Order, id = id)
    res = getOrder(order)
    order.delete()
    return JsonResponse(res, status=status.HTTP_200_OK)


@isAdmin
def getDashboard(request):
    res = {
        "productsCount": Product.objects.all().count(),
        "ordersCount": Order.objects.filter(completed = False).count(),
    }
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


@isAdmin
def getStatistics(request):
    productsStats = {}
    usersStats = {}
    for product in Product.objects.all():
        productsStats[product.id] = {
            "name": product.name,
            "stats": []
        }
    for order in Order.objects.filter(completed = True):
        if usersStats.get(order.phone) == None:
            usersStats[order.phone] = {
                "name": order.username,
                "email": order.email,
                "stats": []
            }
        for orderProduct in OrderProduct.objects.filter(order = order):
            productsStats[orderProduct.product.id]["stats"].append({
                "price": orderProduct.price,
                "date": order.date
            })
            usersStats[order.phone]["stats"].append({
                "price": orderProduct.price,
                "date": order.date
            })

    res = {
        "productsStats": productsStats,
        "usersStats": usersStats,
    }
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)