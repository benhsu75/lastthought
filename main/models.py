from django.db import models

class TestModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    random_number = models.SmallIntegerField()