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

# Represents a user's ridesharing rides
class RideHistoryItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    requested_at = models.DateTimeField()

    rideshare_information = models.ForeignKey(RideshareInformation)

    rideshare_service = models.SmallIntegerField()
    # 0 - lyft
    # 1 - uber

    # Ride info
    ride_id = models.CharField(max_length=200)
    ride_type = models.CharField(max_length=200)

    driver_first_name = models.CharField(max_length=200, null=True)

    # Route info
    origin_address = models.CharField(max_length=200, null=True)
    origin_lat = models.FloatField()
    origin_lng = models.FloatField()

    dest_address = models.CharField(max_length=200, null=True)
    dest_lat = models.FloatField()
    dest_lng = models.FloatField()

    pickup_address = models.CharField(max_length=200, null=True)
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()

    dropoff_address = models.CharField(max_length=200, null=True)
    dropoff_lat = models.FloatField()
    dropoff_lng = models.FloatField()

    # Price info
    price = models.FloatField()
    primetime_percentage = models.IntegerField(null=True)














