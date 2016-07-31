from django.conf.urls import url
from django.contrib import admin
from main import views

urlpatterns = [
    url(r'^$', views.test),
    url(r'^test/', views.test),
    url(r'^test2/', views.test2),
    url(r'^messenger_callback/', views.messenger_callback),
]