from django.conf.urls import url, patterns
from django.contrib import admin
from main import views, goal_views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index),
    url(r'^messenger_callback/', views.messenger_callback),
    url(r'^learn_more/', views.learn_more),

    # Temp helper methods
    url(r'^delete_users/', views.delete_users),

    # Goal endpoints
    url(r'^goals/(?P<fbid>\d+)/$', goal_views.goals),
    url(r'^goals/(?P<fbid>\d+)/list', goal_views.list),
    url(r'^goals/(?P<fbid>\d+)/add', goal_views.add),

]

if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )