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
from eCom_Master.utils import cookieCart, cartData, guestOrder
from eCom_Master.logics import *

def register(request):
    return logics_register(request)


def store(request):
    return logics_store(request)


def cart(request):
    return logics_cart(request)


def checkout(request):
    return logics_checkout(request)


def updateItem(request):
    return logics_updateItem(request)

@csrf_exempt
def processOrder(request):
    return logics_processOrder(request)