from django.db import models

class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fbid = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

# Models for third party connection
class ThirdPartyConnection(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_connected_flag = models.BooleanField(default=False)

class FoursquareConnection(ThirdPartyConnection):
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=1000, null=True) 

class LyftConnection(ThirdPartyConnection):
    user = models.OneToOneField(User)
    refresh_token = models.CharField(max_length=1000, null=True)

class UberConnection(ThirdPartyConnection):
    user = models.OneToOneField(User)
    refresh_token = models.CharField(max_length=1000, null=True)
    
class InstagramConnection(ThirdPartyConnection):
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=1000, null=True)

    instagram_id = models.BigIntegerField()
    username = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=200)

class FitbitConnection(ThirdPartyConnection):
    user = models.OneToOneField(User)
    refresh_token = models.CharField(max_length=1000, null=True)
    fitbit_id = models.CharField(max_length=200)

class GoogleConnection(ThirdPartyConnection):
    user = models.OneToOneField(User)
    refresh_token = models.CharField(max_length=1000, null=True)


# Represents known information about the user
class BackgroundInformation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # General
    locale = models.CharField(max_length=200)
    profile_pic = models.CharField(max_length=200)
    timezone = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)

    # For weather
    current_zip_code = models.CharField(max_length=10, null=True)

    user = models.OneToOneField(User)














