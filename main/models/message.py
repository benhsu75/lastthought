from django.db import models
from user import *
from habit import *


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    sent_to_user = models.BooleanField() # If false, then the message was sent from the user
    message_type = models.SmallIntegerField() # Message types are enumerated in message_log.py

    text = models.CharField(max_length=200, null=True)

    response_captured = models.BooleanField(default=False)
    habit_in_reference = models.ForeignKey(Habit, null=True)