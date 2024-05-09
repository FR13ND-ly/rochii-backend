from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Product
from rest_framework import status
from .serializers import getShortProduct, getProduct
from django.shortcuts import get_object_or_404
from random import sample


def getProducts(request, index):
    products = Product.objects.order_by("-date")
    res = {
        "products": [],
        "more": (products.count() - 10 * (index - 1)) >= 10
    }
    for product in products[10 * (index - 1): 10 * index]:
        res["products"].append(getShortProduct(product))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def getProductDetails(request, id):
    product = get_object_or_404(Product, id = id)
    res = getProduct(product)
    return JsonResponse(res, status=status.HTTP_200_OK)

@csrf_exempt
def getProductsByIds(request):
    data = JSONParser().parse(request)
    res = []
    for id in data:
        product = get_object_or_404(Product, id = id)
        res.append(getProduct(product))
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)


def getSimilarProducts(request, id):
    queryset = Product.objects.exclude(id = id)

    randomProducts = sample(list(queryset), 5)
    
    res = []
    for product in randomProducts:
        res.append(getProduct(product))
    
    return JsonResponse(res, status=status.HTTP_200_OK, safe=False)