from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *

def index(request):
    context = RequestContext(request, {
    })
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(context))

def learn_more(request):
    context = RequestContext(request, {
    })
    template = loader.get_template('main/learn_more.html')
    return HttpResponse(template.render(context))

def delete_users(request):
    all_users = User.objects.all()
    num_of_users_deleted = len(all_users)
    for u in all_users:
        u.delete()
    return HttpResponse("Deleted " + str(num_of_users_deleted) + " users!")

