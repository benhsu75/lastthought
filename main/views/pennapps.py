from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.template import RequestContext, loader

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

def pennapps(request):
    context = RequestContext(request, {
    })
    template = loader.get_template('pennapps.html')
    return HttpResponse(template.render(context))