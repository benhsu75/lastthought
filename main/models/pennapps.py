from django.db import models

class InsulinAmount(models.Model):
    amount = models.FloatField()


class Dose(models.Model):
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    