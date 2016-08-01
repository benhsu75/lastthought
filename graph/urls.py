from django.conf.urls import url
from django.contrib import admin
from main import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^messenger_callback/', views.messenger_callback),
    url(r'^learn_more/', views.learn_more),

    # Temp helper methods
    url(r'^delete_users/', views.delete_users),
]