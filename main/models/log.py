from django.db import models
from user import *


# for now every user only has one log
class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)

    @staticmethod
    def find_or_create(current_user):
        user_log = Log.objects.filter(user=current_user)
        if len(user_log) == 1:
            user_log = user_log[0]
        elif len(user_log) == 0:
            user_log = Log(user=current_user)
            user_log.save()
        return user_log


class LogContext(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    log = models.ForeignKey(Log)

    context_name = models.CharField(max_length=200)

class LogEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    log = models.ForeignKey(Log)
    log_context = models.ForeignKey(LogContext, blank=True, null=True)

    entry_type = models.SmallIntegerField()
    # 0 - text
    # 1 - numeric
    # 2 - image

class TextLogEntry(LogEntry):
    text_value = models.CharField(max_length=10000)

class NumericLogEntry(LogEntry):
    numeric_value = models.FloatField(default=0)

class ImageLogEntry(LogEntry):
    image_url = models.CharField(max_length=1000)
    image_width = models.SmallIntegerField()
    image_height = models.SmallIntegerField()

