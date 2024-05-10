from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Product
from rest_framework import status
from .serializers import getShortProduct, getProduct
from django.shortcuts import get_object_or_404
from random import sample
from django.core.paginator import Paginator

def getProducts(request, index):
    page_size = 10 
    products = Product.objects.order_by("-date")

    paginator = Paginator(products, page_size)
    try:
        page = paginator.page(index)
    except:
        return JsonResponse({'error': 'Invalid page index'}, status=status.HTTP_400_BAD_REQUEST)

    short_products = [getShortProduct(product) for product in page.object_list]

    return JsonResponse({
        "products": short_products,
        "more": page.has_next()
    }, status=status.HTTP_200_OK, safe=False)


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