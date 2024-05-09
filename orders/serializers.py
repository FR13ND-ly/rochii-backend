from .models import Order, OrderProduct
from products.models import ProductImage
from files.views import getImage

def getOrder(order: Order):
    res = {
        "id": order.id,
        "username": order.username,
        "phone": order.phone,
        "email": order.email,
        "details": order.details,
        "completed": order.completed,
        "date": order.date,
        "hour": order.hour,
        "createdDate": order.createdDate,
        "products": []   
    }
    for orderProduct in OrderProduct.objects.filter(order = order):
        res["products"].append({
            "name" : orderProduct.product.name,
            "description": orderProduct.product.description,
            "mainImg": getImage(ProductImage.objects.get(product = orderProduct.product, main = True).image),
            "price": orderProduct.price,
        })
    return res