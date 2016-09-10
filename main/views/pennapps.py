from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.template import RequestContext, loader
from main.models import *

@csrf_exempt
def get_insulin_amount(request):
    # TODO
    return HttpResponse('2')

@csrf_exempt
def log_insulin(request):
    # TODO
    x = 1
    return HttpResponse(status=200)

@csrf_exempt
def get_insulin_logs(request):
    # TODO
    x = 1

@csrf_exempt
def set_insulin_amount(request):
    amount = request.POST['amount']

    try:
        insulin_amount = InsulinAmount.objects.all().first()

        if not insulin_amount:
            insulin_amount = InsulinAmount(amount=amount)
            insulin_amount.save()
        else:
            insulin_amount.amount = amount;
            insulin_amount.save()
    except InsulinAmount.DoesNotExist: 
        insulin_amount = InsulinAmount(amount=amount)
        insulin_amount.save()

    return HttpResponse(status=200)

def pennapps(request):
    try:
        insulin_amount = InsulinAmount.objects.first()

        if not insulin_amount:
            amount = 0.0
        else:
            amount = insulin_amount.amount
    except InsulinAmount.DoesNotExist:
        amount = 0.0


    context = RequestContext(request, {
        'amount' : amount 
    })
    template = loader.get_template('pennapps.html')
    return HttpResponse(template.render(context))