from django.db import models
from user import *


class ToDoTask(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    text = models.CharField(max_length=300)

    completed = models.BooleanField(default=False)
