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

    # For ridesharing
    current_home_address = models.CharField(max_length=200, null=True)
    current_work_address = models.CharField(max_length=200, null=True)
    ride_type_preference = models.SmallIntegerField(null=True)

    user = models.OneToOneField(User)