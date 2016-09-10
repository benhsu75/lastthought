from django.db import models
import datetime
from django.utils.timesince import timesince
import pytz
import math

class InsulinAmount(models.Model):
    amount = models.FloatField()

class Dose(models.Model):
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_time_diff_from_now(self):
        now = datetime.datetime.now()

        diff_in_min = (now - self.created_at.replace(tzinfo=None)).seconds//60

        if diff_in_min >= 60:
            to_return = str(int(math.ceil(diff_in_min/60.0))) + ' hours'
        else:
            to_return = str(diff_in_min) + ' minutes'

        return to_return

class GlucoseLog(models.Model):
    level = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
