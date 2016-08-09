from django.db import models

class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fbid = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

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

    lyft_access_token = models.CharField(max_length=100, null=True)
    lyft_refresh_token = models.CharField(max_length=100, null=True)

    ride_type_preference = models.CharField(max_length=100, null=True)
    # Can be lyft_line, lyft, or lyft_plus

    # Home and work text
    current_home_address = models.CharField(max_length=200, null=True)
    current_work_address = models.CharField(max_length=200, null=True)

    # Home and work lat and longs
    home_lat = models.FloatField(null=True)
    home_long = models.FloatField(null=True)
    work_lat = models.FloatField(null=True)
    work_long = models.FloatField(null=True)

    # True if either Lyft or Uber is connected
    connected_flag = models.BooleanField(default=False)