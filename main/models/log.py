from django.db import models
from user import *


# for now every user only has one log
class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    profile = models.ForeignKey(Profile)

    @staticmethod
    def find_or_create(current_profile):
        profile_log = Log.objects.filter(profile=current_profile)
        if len(profile_log) == 1:
            profile_log = profile_log[0]
        elif len(profile_log) == 0:
            profile_log = Log(profile=current_profile)
            profile_log.save()
        return profile_log


class LogContext(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    log = models.ForeignKey(Log)

    context_name = models.CharField(max_length=200)


class LogEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    occurred_at = models.DateTimeField()

    log = models.ForeignKey(Log)
    log_context = models.ForeignKey(LogContext, blank=True, null=True)

    entry_type = models.SmallIntegerField()
    # 0 - text
    # 1 - numeric
    # 2 - image
    # 3 - Lyft ride
    # 4 - Venue checkin
    # 5 - Instagram
    # 6 - Weight
    # 7 - Activity

    def occurred_at_display_string(self):
        # imports
        from datetime import datetime, timedelta
        import pytz

        difference = datetime.utcnow().replace(
            tzinfo=pytz.utc
        ) - self.occurred_at

        # If within 60 min, show "X min ago"
        if difference < timedelta(hours=1):
            min_diff = difference.seconds // 60
            if min_diff == 1:
                min_string = 'minute'
            else:
                min_string = 'minutes'
            display_string = '{} {} ago'.format(min_diff, min_string)
            return display_string

        # If within 24 hours, show "X hours ago"
        elif difference < timedelta(hours=24):
            hours_diff = difference.seconds // 3600
            if hours_diff == 1:
                hour_string = 'hour'
            else:
                hour_string = 'hours'
            display_string = '{} {} ago'.format(hours_diff, hour_string)
            return display_string

        # If within 1 week, show "X days ago"
        elif difference < timedelta(days=7):
            days_diff = difference.days
            if days_diff == 1:
                day_string = 'day'
            else:
                day_string = 'days'
            display_string = '{} {} ago'.format(days_diff, day_string)
            return display_string

        # Else, show the day

        # Get utc_offset from profile

        utc_offset = self.log.profile.utc_offset
        offset_timedelta = timedelta(hours=utc_offset)

        old_occurred_at = self.occurred_at

        localized_occurred_at = old_occurred_at + offset_timedelta

        local_date = localized_occurred_at

        display_string = local_date.strftime("%B %d, %Y")

        return display_string


class TextLogEntry(LogEntry):
    text_value = models.CharField(max_length=10000)

    def is_link(self):
        import re
        regex = re.compile(
            (
                'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]'
                '|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

            ), re.IGNORECASE
        )

        return regex.match(self.text_value) is not None


class NumericLogEntry(LogEntry):
    numeric_value = models.FloatField(default=0)


class ImageLogEntry(LogEntry):
    image_url = models.CharField(max_length=1000)
    image_width = models.SmallIntegerField()
    image_height = models.SmallIntegerField()


class RideLogEntry(LogEntry):
    requested_at = models.DateTimeField()
    rideshare_service = models.SmallIntegerField()
    # 0 - lyft
    # 1 - uber

    distance = models.FloatField(null=True)
    city_name = models.CharField(max_length=200, null=True)
    city_lat = models.FloatField(null=True)
    city_lng = models.FloatField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    start_city_name = models.CharField(max_length=200, null=True)
    start_city_lat = models.FloatField(null=True)
    start_city_lng = models.FloatField(null=True)

    # Ride info
    ride_id = models.CharField(max_length=200)
    ride_type = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    driver_first_name = models.CharField(max_length=200, null=True)

    # Route info
    origin_address = models.CharField(max_length=200, null=True)
    origin_lat = models.FloatField(null=True)
    origin_lng = models.FloatField(null=True)

    dest_address = models.CharField(max_length=200, null=True)
    dest_lat = models.FloatField(null=True)
    dest_lng = models.FloatField(null=True)

    pickup_address = models.CharField(max_length=200, null=True)
    pickup_lat = models.FloatField(null=True)
    pickup_lng = models.FloatField(null=True)

    dropoff_address = models.CharField(max_length=200, null=True)
    dropoff_lat = models.FloatField(null=True)
    dropoff_lng = models.FloatField(null=True)

    # Price info
    price_in_dollars = models.FloatField(null=True)
    primetime_percentage = models.IntegerField(null=True)


class VenueLogEntry(LogEntry):
    source_type = models.SmallIntegerField()
    # 0 - Foursquare
    # Others...

    foursquare_id = models.CharField(max_length=200, null=True)

    lat = models.FloatField()
    lng = models.FloatField()
    formatted_address = models.CharField(max_length=500)

    name = models.CharField(max_length=200)

    comment = models.CharField(max_length=1000, null=True)

    img_url_prefix = models.CharField(max_length=200, null=True)
    img_url_suffix = models.CharField(max_length=200, null=True)
    img_dim_width = models.SmallIntegerField(null=True)
    img_dim_height = models.SmallIntegerField(null=True)


class InstagramLogEntry(LogEntry):
    instagram_id = models.CharField(max_length=100)
    likes = models.SmallIntegerField()

    link_to_post = models.CharField(max_length=200)

    thumbnail_url = models.CharField(max_length=200)
    thumbnail_height = models.SmallIntegerField()
    thumbnail_width = models.SmallIntegerField()

    low_res_url = models.CharField(max_length=200)
    low_res_height = models.SmallIntegerField()
    low_res_width = models.SmallIntegerField()

    high_res_url = models.CharField(max_length=200)
    high_res_height = models.SmallIntegerField()
    high_res_width = models.SmallIntegerField()

    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    location_name = models.CharField(max_length=200)

    caption = models.CharField(max_length=1000, null=True)


class WeightLogEntry(LogEntry):
    source_type = models.SmallIntegerField()
    # 0 - Fitbit
    # others...

    metric_weight = models.FloatField()

    source_id = models.CharField(max_length=200)


class ActivityLogEntry(LogEntry):
    source_type = models.SmallIntegerField()
    # 0 - Fitbit
    # Others...

    num_steps = models.IntegerField(null=True)
    distance_km = models.FloatField(null=True)
    num_calories = models.IntegerField(null=True)
