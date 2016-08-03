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

# View methods
def list(request, fbid):
    if not user_exists(fbid):
        return HttpResponse(status=404)

    current_user = User.objects.get(fbid=fbid)
    todo_list = ToDoTask.objects.filter(user=current_user)

    context = RequestContext(request, {
        'todo_list': todo_list,
        'fbid' : fbid
    })
    template = loader.get_template('todo/list.html')
    return HttpResponse(template.render(context))

# REST endpoints
def todo(request, todo_id):

    todo = ToDoTask.objects.get(id=todo_id)

    # Get list of all todo's
    if request.method == 'GET':
        serialized_response = serializers.serialize('json', [todo])
        return HttpResponse(serialized_response)

    elif request.method == 'DELETE':
        todo.delete()
        return HttpResponse(status=200)
    # Error 404 Not Found
    else:
        return HttpResponse(status=404)

def add_todo(request):
    # Create new todo
    if request.method == 'POST':
        fbid = request.POST['fbid']
        text = request.POST['text']
        current_user = User.objects.get(fbid=fbid)

        todo = ToDoTask(text=text, user=current_user)
        todo.save()

        return HttpResponse(status=200)
    # Error 404 Not Found
    else:
        return HttpResponse(status=404)







