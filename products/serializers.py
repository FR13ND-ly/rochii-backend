from .models import ProductImage
from files.views import getImage

def getShortProduct(product):
    res = {
        "id": product.id,
        "name": product.name,
        "mainImg": getImage(ProductImage.objects.get(product = product, main = True).image),
    }
    return res


def getProduct(product):
    res = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "date": product.date,
        "mainImg": "",
        "images": []
    }
    for productImage in ProductImage.objects.filter(product = product):
        if productImage.main:
            res["mainImg"] = getImage(productImage.image)
        else:
            res["images"].append(getImage(productImage.image))
    return res