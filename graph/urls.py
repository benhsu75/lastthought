from django.conf.urls import url, patterns
from django.contrib import admin
from main.views import general, habit_views, log_views
from main.entrypoints.messenger import messenger
from django.conf import settings

urlpatterns = [
    url(r'^$', general.index),

    # Static pages
    url(r'^learn_more/', general.learn_more),

    # Messenger webhooks
    url(r'^messenger_callback/', messenger.messenger_callback),

    # Facebook Login redirect
    url(r'^fblogin_redirect/', general.fblogin_redirect),
    
    # Habit endpoints
    url(r'^habits/(?P<habit_id>\d+)/$', habit_views.habits),
    url(r'^habits/$', habit_views.habits),

    # Log endpoints
    url(r'^logs/(?P<logentry_id>\d+)/$', log_views.logs),
    url(r'^logs/$', log_views.logs),
    url(r'^log_contexts/(?P<logcontext_id>\d+)/$', log_views.log_contexts),

    # Display endpoints
    url(r'^users/(?P<fbid>\d+)/habits$', habit_views.list),
    url(r'^users/(?P<fbid>\d+)/add_habit', habit_views.add_habit_page),
    url(r'^users/(?P<fbid>\d+)/habits/(?P<habit_id>\d+)/show', habit_views.show),
    url(r'^users/(?P<fbid>\d+)/logs', log_views.index),
    url(r'^users/(?P<fbid>\d+)/log_context/(?P<log_context_id>\d+)', log_views.log_context_show),

]

# Ensure static files are accessible
if True:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )