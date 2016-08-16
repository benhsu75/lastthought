from django.db import models
from user import *
from habit import *


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)

    # If false, then the message was sent from the user
    sent_to_user = models.BooleanField()

    # Message types are enumerated in message_log.py
    message_type = models.SmallIntegerField(null=False)
    text = models.CharField(max_length=2000, null=True)

    habit_entry_in_reference = models.ForeignKey(HabitEntry, null=True)
