from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.template import RequestContext, loader
from main.models import *

@csrf_exempt
def get_insulin_amount(request):

    # Get the insulin amount
    insulin_amount = InsulinAmount.objects.first()

    if not insulin_amount:
        insulin_amount = InsulinAmount(amount=0.0)
        insulin_amount.save()

    return HttpResponse(insulin_amount.amount)

@csrf_exempt
def log_insulin(request):
    # Get insulin amount
    insulin_amount = InsulinAmount.objects.first()

    if not insulin_amount:
        insulin_amount = InsulinAmount(amount=0.0)
        insulin_amount.save()

    # Create log
    dose = Dose(amount=insulin_amount.amount)
    dose.save()
    
    return HttpResponse(status=200)

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
        'amount' : amount,
        'doses' : Dose.objects.all().order_by('-created_at'),
        'last_dose_amount' : Dose.objects.all().order_by('-created_at').first().amount,
        'last_dose_time' : Dose.objects.all().order_by('-created_at').first().get_time_diff_from_now
    })
    template = loader.get_template('pennapps.html')
    return HttpResponse(template.render(context))