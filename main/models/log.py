from django.db import models
from user import *


class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    send_text = models.CharField(max_length=200)
    send_time_utc = models.SmallIntegerField(null=True)
    response_type = models.SmallIntegerField()
    # 0 = Text
    # 1 = Picture
    # 2 = Numeric
    
class LogEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    log = models.ForeignKey(Log)

    numeric_value = models.FloatField(null=True)
    binary_value = models.SmallIntegerField(null=True) # 0 = False, 1 = True
    text_value = models.CharField(max_length=1000, null=True)
    response_collected = models.SmallIntegerField(default=0)