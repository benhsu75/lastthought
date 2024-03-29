from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    fbid = models.CharField(max_length=200)
    global_fbid = models.CharField(max_length=200, null=True)

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    email = models.CharField(max_length=200, null=True)

    utc_offset = models.IntegerField()

    send_reminders_flag = models.BooleanField(default=True)

    reminder_settings = models.IntegerField()
    # 0 - Default - send daily
    # 1 - Send weekly
    # 2 - Don't send any


# Models for third party connection
class ThirdPartyConnection(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_connected_flag = models.BooleanField(default=False)


class FoursquareConnection(ThirdPartyConnection):
    user = models.OneToOneField(Profile)
    access_token = models.CharField(max_length=1000, null=True)


class LyftConnection(ThirdPartyConnection):
    user = models.OneToOneField(Profile)
    refresh_token = models.CharField(max_length=1000, null=True)


class UberConnection(ThirdPartyConnection):
    user = models.OneToOneField(Profile)
    refresh_token = models.CharField(max_length=1000, null=True)


class InstagramConnection(ThirdPartyConnection):
    user = models.OneToOneField(Profile)
    access_token = models.CharField(max_length=1000, null=True)

    instagram_id = models.BigIntegerField()
    username = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=200)


class FitbitConnection(ThirdPartyConnection):
    user = models.OneToOneField(Profile)
    refresh_token = models.CharField(max_length=1000, null=True)
    fitbit_id = models.CharField(max_length=200)


class GoogleConnection(ThirdPartyConnection):
    user = models.OneToOneField(Profile)
    refresh_token = models.CharField(max_length=1000, null=True)
