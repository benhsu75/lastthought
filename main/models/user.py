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

    instagram_id = models.IntegerField()
    username = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=200)

#

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

# Represents all the ridesharing information known about a user
class RideshareInformation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    lyft_refresh_token = models.CharField(max_length=500, null=True)

    ride_type_preference = models.CharField(max_length=100, null=True)
    # Can be lyft_line, lyft, or lyft_plus

    # Home and work text
    current_home_address = models.CharField(max_length=200, null=True)
    current_work_address = models.CharField(max_length=200, null=True)

    # Home and work lat and longs
    home_lat = models.FloatField(null=True)
    home_lng = models.FloatField(null=True)
    work_lat = models.FloatField(null=True)
    work_lng = models.FloatField(null=True)

    # True if either Lyft is connected
    lyft_connected_flag = models.BooleanField(default=False)

    uber_connected_flag = models.BooleanField(default=False)

    # True if the user wants us to send them a commute button
    send_ride_button_flag = models.BooleanField(default=True)

    # Preferred rideshare company
    rideshare_service_preference = models.SmallIntegerField(default=0)
    # 0 - Lyft
    # 1 - Uber

    user = models.OneToOneField(User)













