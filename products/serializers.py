from .models import ProductImage
from files.views import getImage

def getShortProduct(product):
    res = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "date": product.date,
        "mainImg": getImage(ProductImage.objects.get(product = product, main = True).image),
    }
    return res


def getProduct(product):
    product_images = ProductImage.objects.filter(product=product)

    main_img = None
    images = []
    for product_image in product_images:
        if product_image.main:
            main_img = getImage(product_image.image)
        else:
            images.append(getImage(product_image.image))

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "date": product.date,
        "mainImg": main_img,
        "images": images
    }