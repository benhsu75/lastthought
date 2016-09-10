from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def get_insulin_amount(request):
    # TODO
    return HttpResponse('2')

@csrf_exempt
def log_insulin(request):
    # TODO
    x = 1
    return HttpResponse(status=200)