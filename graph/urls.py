from django.conf.urls import url, patterns
from django.contrib import admin
from main.views import general, habit_views, todo_views, log_views, ridesharing_views
from main.entrypoints.messenger import messenger
from django.conf import settings

urlpatterns = [
    url(r'^$', general.index),
    url(r'^messenger_callback/', messenger.messenger_callback),
    url(r'^learn_more/', general.learn_more),

    # Temp helper methods
    url(r'^delete_users/', general.delete_users),
    url(r'^delete_all/', general.delete_all),

    # Habit endpoints
    url(r'^habits/(?P<habit_id>\d+)/$', habit_views.habits),
    url(r'^habits/$', habit_views.habits),

    # Log endpoints
    url(r'^logs/(?P<logentry_id>\d+)/$', log_views.logs),
    url(r'^logs/$', log_views.logs),

    # Todo endpoints
    url(r'^todo/(?P<todo_id>\d+)/$', todo_views.todo),
    url(r'^todo/$', todo_views.todo),

    # Display endpoints
    url(r'^users/(?P<fbid>\d+)/$', general.dashboard),
    url(r'^users/(?P<fbid>\d+)/todo', todo_views.list),
    url(r'^users/(?P<fbid>\d+)/habits', habit_views.list),
    url(r'^users/(?P<fbid>\d+)/add_habit', habit_views.add_habit_page),
    url(r'^habits/(?P<habit_id>\d+)/show', habit_views.show),
    url(r'^users/(?P<fbid>\d+)/setup_ridesharing', ridesharing_views.setup),

]

# Ensure static files are accessible
if True:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )