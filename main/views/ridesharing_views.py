from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *


def setup(request, fbid):
    context = RequestContext(request, {})
    template = loader.get_template('main/ridesharing_setup.html')
    return HttpResponse(template.render(context))


