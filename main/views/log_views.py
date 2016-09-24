from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *

from django.shortcuts import redirect
import json
from django.core import serializers
from main.utils import helper_util
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime
from django.core.paginator import Paginator


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

# For pagination
NUM_ENTRIES_PER_PAGE = 20

# View methods
def index(request, fbid, page_no):
    # Check if user is authenticated
    # if not request.user.is_authenticated():
    #     return redirect('/')

    # Get user
    if helper_util.profile_exists(fbid):
        current_profile = Profile.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=200)

    # Get log for this user
    user_log = Log.find_or_create(current_profile)

    log_context_list = LogContext.objects.filter(log=user_log).order_by('context_name')

    # Pagination
    log_entry_list = LogEntry.objects.filter(
        log=user_log
    ).order_by('-occurred_at')

    p = Paginator(log_entry_list, NUM_ENTRIES_PER_PAGE)
    num_pages = p.num_pages
    print 'Num Pages: ' + str(num_pages) 
    current_page = p.page(page_no)

    has_prev = current_page.has_previous()
    has_next = current_page.has_next()

    prev_page_no = -1
    next_page_no = -1
    if has_prev:
        prev_page_no = current_page.previous_page_number()
    if has_next:
        next_page_no = current_page.next_page_number()

    current_log_entry_list = current_page.object_list

    context = RequestContext(request, {
        'fbid': fbid,
        'log_context_list': log_context_list,
        'log_entry_list': current_log_entry_list,
        'has_prev' : has_prev,
        'has_next' : has_next,
        'prev_page_no' : prev_page_no,
        'next_page_no' : next_page_no
    })
    template = loader.get_template('log/index.html')
    return HttpResponse(template.render(context))


# View methods
def indexTest(request, fbid):

    # Get user
    if helper_util.profile_exists(fbid):
        current_profile = Profile.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=200)

    # Get log for this user
    user_log = Log.find_or_create(current_profile)

    log_context_list = LogContext.objects.filter(log=user_log)

    today = date.today()
    date_numbers = today.isocalendar()
    beg_week = datetime.strptime(
        str(date_numbers[0]) + '-W' + str(date_numbers[1]-1) + '-0',
        "%Y-W%W-%w"
    )
    end_week = datetime.strptime(
        str(date_numbers[0]) + '-W' + str(date_numbers[1]) + '-0',
        "%Y-W%W-%w"
    )

    print(beg_week.strftime("%B %d, %Y"))
    print(end_week)
    print(today.strftime("%B %d, %Y"))

    log_entry_list = LogEntry.objects.filter(
        log=user_log
    ).order_by('-occurred_at')

    context = RequestContext(request, {
        'fbid': fbid,
        'log_context_list': log_context_list,
        'log_entry_list': log_entry_list,
        'start_date': beg_week.strftime("%B %d, %Y"),
        'today_date': today.strftime("%B %d, %Y"),
    })
    template = loader.get_template('log/index.html')
    return HttpResponse(template.render(context))


def log_context_show(request, log_context_id):
    # Get user
    if not helper_util.authenticated_and_profile_exists(request):
        return redirect('/')
    
    # Get page number
    if 'page' in request.GET:
        page_no = request.GET['page']
    else:
        page_no = 1

    # Authenticate
    fbid = request.user.profile.fbid
    if helper_util.profile_exists(fbid):
        current_profile = Profile.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=200)

    # Get log for this user
    user_log = Log.find_or_create(current_profile)

    # Get objects
    log_context = LogContext.objects.get(id=log_context_id)

    # Pagination
    log_entry_list = LogEntry.objects.filter(
        log=user_log,
        log_context=log_context
    ).order_by('-occurred_at')

    p = Paginator(log_entry_list, NUM_ENTRIES_PER_PAGE)
    num_pages = p.num_pages
    current_page = p.page(page_no)

    has_prev = current_page.has_previous()
    has_next = current_page.has_next()

    prev_page_no = -1
    next_page_no = -1
    if has_prev:
        prev_page_no = current_page.previous_page_number()
    if has_next:
        next_page_no = current_page.next_page_number()

    current_log_entry_list = current_page.object_list

    context = RequestContext(request, {
        'log_context': log_context,
        'fbid': fbid,
        'log_entry_list': current_log_entry_list,
        'has_prev' : has_prev,
        'has_next' : has_next,
        'prev_page_no' : prev_page_no,
        'next_page_no' : next_page_no
    })
    template = loader.get_template('log/log_context.html')
    return HttpResponse(template.render(context))
