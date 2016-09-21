from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *

import json
from django.core import serializers
from main.utils import helper_util
from django.views.decorators.csrf import csrf_exempt

# Helper methods

def get_log_entry(log_entry_id):
    if log_entry_id is None:
        return None
    try:
        log_entry = LogEntry.objects.get(id=log_entry_id)
        return log_entry
    except LogEntry.DoesNotExist:
        return None

def get_log_context(log_context_id):
    if log_context_id is None:
        return None
    try:
        log_context = LogContext.objects.get(id=log_context_id)
        return log_context
    except LogContext.DoesNotExist:
        return None

# Endpoint methods
@csrf_exempt
def logs(request, logentry_id=None):
    if request.method == 'GET':
        return HttpResponse("GET LOGS", status=200)
    elif request.method == 'POST':
        return HttpResponse(status=200)
    elif request.method == 'DELETE':
        log_entry = get_log_entry(logentry_id)

        log_entry.delete()

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)

@csrf_exempt
def log_contexts(request, logcontext_id=None):
    if request.method == 'GET':
        return HttpResponse("GET LOGS", status=200)
    elif request.method == 'POST':
        return HttpResponse(status=200)
    elif request.method == 'DELETE':

        log_context = get_log_context(logcontext_id)

        # Remove all relations to this log context
        log_entries = LogEntry.objects.filter(log_context=log_context)
        for l_e in log_entries:
            l_e.log_context = None
            l_e.save()
        
        log_context.delete()

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)

# View methods

def index(request, fbid):
    # Get user
    if helper_util.profile_exists(fbid):
        current_profile = Profile.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=200)

    # Get log for this user
    user_log = Log.find_or_create(current_profile)

    log_context_list = LogContext.objects.filter(log=user_log)

    # TODO PAGINATION, but for interim, limit results so page doesn't load SUPER slowly
    log_entry_list = LogEntry.objects.filter(log=user_log).order_by('-occurred_at')[:100]  
    
    context = RequestContext(request, {
        'fbid': fbid,
        'log_context_list' : log_context_list,
        'log_entry_list' : log_entry_list
    })
    template = loader.get_template('log/index.html')
    return HttpResponse(template.render(context))

def log_context_show(request, fbid, log_context_id):
     # Get user
    if helper_util.profile_exists(fbid):
        current_profile = Profile.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=200)

    # Get log for this user
    user_log = Log.find_or_create(current_profile)

    # Get objects
    log_context = LogContext.objects.get(id=log_context_id)

    log_entry_list = LogEntry.objects.filter(log=user_log, log_context=log_context).order_by('-occurred_at')

    context = RequestContext(request, {
        'fbid': fbid,
        'log_context' : log_context,
        'log_entry_list' : log_entry_list
    })
    template = loader.get_template('log/log_context.html')
    return HttpResponse(template.render(context))


