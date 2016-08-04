from django.conf.urls import url, patterns
from django.contrib import admin
from main import views, goal_views, todo_views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index),
    url(r'^messenger_callback/', views.messenger_callback),
    url(r'^learn_more/', views.learn_more),

    # Temp helper methods
    url(r'^delete_users/', views.delete_users),

    # Goal endpoints
    url(r'^goals/(?P<goal_id>\d+)/$', goal_views.goals),
    url(r'^goals/$', goal_views.goals),
    
    # Todo endpoints
    url(r'^todo/(?P<todo_id>\d+)/$', todo_views.todo),
    url(r'^todo/$', todo_views.todo),

    # Display endpoints
    url(r'^users/(?P<fbid>\d+)/todo', todo_views.list),
    url(r'^users/(?P<fbid>\d+)/goals', goal_views.list),
    url(r'^users/(?P<fbid>\d+)/add_goal', goal_views.add_goal_page),
    url(r'^goals/(?P<goal_id>\d+)/show', goal_views.show),

]

# Ensure static files are accessible
if True:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )