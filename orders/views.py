from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from products.models import Product
from .models import Order, OrderProduct
from rest_framework import status
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .serializers import getOrder
from datetime import datetime


@csrf_exempt
def getAvailableHours(request):
    data = JSONParser().parse(request)
    date = formatDate(data)
    bookedHours = Order.objects.filter(date=date).values_list('hour', flat=True)
    res = [hour for hour in range(8, 15) if hour not in bookedHours]
    return JsonResponse(res, status=status.HTTP_201_CREATED, safe=False)


@csrf_exempt
def createOrder(request):
    data = JSONParser().parse(request)
    order = Order.objects.create(
        username = data["username"],
        phone = data["phone"],
        email = data["email"],
        date = formatDate(data['date']),
        hour = data['hour'],
        details = data["details"]
    )
    details = {
        "date": order.date,
        "hour": str(order.hour) + ":00",
        "name": order.username,
        "email": order.email,
        "phone": order.phone,
        "details": order.details,
        "products": []
    }
    order.save()
    for product in data["products"]:
        p = Product.objects.get(id = product["id"])
        details["products"].append({
            "name": p.name,
            "price": p.price,
        })
        orderProduct = OrderProduct.objects.create(
            order = order,
            product = p,
            price = p.price
        )
        orderProduct.save()
    res = getOrder(order)
    # sendEmails(details)
    return JsonResponse(res, status=status.HTTP_201_CREATED)


def formatDate(date):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').date()


def sendEmails(details):
    if details["email"] == "": return
    subject = 'Programare nouă'
    orderMessage = render_to_string('order_notification.html', details)
    customerMessage = render_to_string('customer_notification.html', details)
    send_mail(
        subject = subject, 
        message="",
        html_message=customerMessage, 
        from_email='contact@bride2beboutique.ro', 
        recipient_list=[details["email"]]
    )
    send_mail(
        subject = subject, 
        message="",
        html_message=orderMessage, 
        from_email='contact@bride2beboutique.ro', 
        recipient_list=[settings.EMAIL_RECEIVER]
    )