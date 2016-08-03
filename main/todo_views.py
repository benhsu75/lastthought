from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *

import json
from django.core import serializers

# Helper method
def user_exists(fbid):
    try:
        user = User.objects.get(fbid=fbid)
        return True
    except User.DoesNotExist:
        return False

def index(request, fbid):
    if not user_exists(fbid):
        return HttpResponse(status=404)

    current_user = User.objects.get(fbid=fbid)