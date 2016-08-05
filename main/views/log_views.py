from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *

import json
from django.core import serializers
from main.utils import helper_util

def logs(request, log_id=None):

    if request.method == 'GET':
        return HttpResponse(status=200)
    elif request.method == 'DELETE':
        return HttpResponse(status=200)

    elif request.method == 'POST':
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)