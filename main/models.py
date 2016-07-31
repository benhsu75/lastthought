from django.db import models

class TestModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    random_number = models.SmallIntegerField()

class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fbid = models.CharField(max_length=200)
    state = models.SmallIntegerField()

# User States
# 0 - Onboarding after initial message

class Goal(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fbid = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    send_text = models.CharField(max_length=200)
    send_time_utc = models.SmallIntegerField(null=True)

    # 0 = Numeric
    # 1 = Binary
    # 2 = Text
    # 3 = File
    response_type = models.SmallIntegerField()

class GoalEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    goal = models.ForeignKey(Goal)

    numeric_value = models.FloatField(null=True)
    binary_value = models.BooleanField(default=False)
    text_value = models.CharField(max_length=1000)


