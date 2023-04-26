from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import *
from .utils import cookieCart, cartData, guestOrder

def register(request):
    form=UserCreationForm
    if request.method=='POST':
        regForm=UserCreationForm(request.POST)
        if regForm.is_valid():
            regForm.save()
    return render(request, 'registration/register.html', {'form':form})


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    user = request.user

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'user': user}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer, order = guestOrder(request, data)
    else:
        customer, order = guestOrder(request, data)
    
    message = Mail(
        from_email='abhishekmalik2903@gmail.com',
        to_emails=customer.email,
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)