from django.db import models
from user import *


# for now every user only has one log
class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)

    name = models.CharField(max_length=200)
    # 0: Text
    # 1: Picture
    # 2: Numeric
    log_type = models.SmallIntegerField()


class LogContext(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    log = models.ForeignKey(Log)

    context_name = models.CharField(max_length=200)


class TextLogEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    log = models.ForeignKey(Log)
    log_context = models.ForeignKey(LogContext, blank=True, null=True)

    text_value = models.CharField(max_length=1000)


class NumericLogEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    log = models.ForeignKey(Log)
    # doesn't make sense for numeric log to not have a context
    log_context = models.ForeignKey(LogContext, blank=False, null=False)

    text_value = models.FloatField(default=0)
