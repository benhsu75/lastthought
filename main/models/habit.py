from django.db import models
from user import *

class Habit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    profile = models.ForeignKey(Profile)
    name = models.CharField(max_length=200)
    send_text = models.CharField(max_length=200)
    send_time_utc = models.SmallIntegerField(null=True)
    response_type = models.SmallIntegerField()
    # 0 = Numeric
    # 1 = Binary
    # 2 = Text
    # 3 = File
    
class HabitEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    habit = models.ForeignKey(Habit)

    numeric_value = models.FloatField(null=True)
    binary_value = models.SmallIntegerField(null=True) # 0 = False, 1 = True
    text_value = models.CharField(max_length=1000, null=True)
    
    response_collected = models.SmallIntegerField(default=0)
