from django.conf.urls import url, patterns
from django.contrib import admin
from main.views import general, habit_views, todo_views, log_views, ridesharing_views
from main.entrypoints.messenger import messenger
from django.conf import settings
from main.domains import ridesharing_domain

urlpatterns = [
    url(r'^$', general.index),

    # Static pages
    url(r'^learn_more/', general.learn_more),

    # Messenger webhooks
    url(r'^messenger_callback/', messenger.messenger_callback),

    # Ridesharing endpoints
    url(r'^lyft_redirect/', ridesharing_domain.lyft_redirect), # lyft webhook
    url(r'^rideshare_information/', ridesharing_views.rideshare_information),
    url(r'^users/(?P<fbid>\d+)/request_ride', ridesharing_views.request_ride),
    url(r'^users/(?P<fbid>\d+)/ride_history', ridesharing_views.ride_history),

    # Temp helper methods
    url(r'^delete_users/', general.delete_users),
    url(r'^delete_all/', general.delete_all),

    # Habit endpoints
    url(r'^habits/(?P<habit_id>\d+)/$', habit_views.habits),
    url(r'^habits/$', habit_views.habits),

    # Log endpoints
    url(r'^logs/(?P<logentry_id>\d+)/$', log_views.logs),
    url(r'^logs/$', log_views.logs),
    url(r'^log_contexts/(?P<logcontext_id>\d+)/$', log_views.log_contexts),

    # Todo endpoints
    url(r'^todo/(?P<todo_id>\d+)/$', todo_views.todo),
    url(r'^todo/$', todo_views.todo),

    # Display endpoints
    url(r'^users/(?P<fbid>\d+)/$', general.dashboard),
    url(r'^users/(?P<fbid>\d+)/todo', todo_views.list),
    url(r'^users/(?P<fbid>\d+)/habits$', habit_views.list),
    url(r'^users/(?P<fbid>\d+)/connect$', general.connect),
    url(r'^users/(?P<fbid>\d+)/add_habit', habit_views.add_habit_page),
    url(r'^users/(?P<fbid>\d+)/habits/(?P<habit_id>\d+)/show', habit_views.show),
    url(r'^users/(?P<fbid>\d+)/setup_ridesharing', ridesharing_views.setup),
    url(r'^users/(?P<fbid>\d+)/logs', log_views.index),
    url(r'^users/(?P<fbid>\d+)/log_context/(?P<log_context_id>\d+)', log_views.log_context_show),

]

# Ensure static files are accessible
if True:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )