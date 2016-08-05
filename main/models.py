from django.db import models


class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fbid = models.CharField(max_length=200)
    state = models.SmallIntegerField()
    full_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)

    active_goal_entry = models.ForeignKey('GoalEntry', default=None, null=True)

# User States
# 0 - Onboarding after initial messages
# 1 - Neutral state

class Goal(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    send_text = models.CharField(max_length=200)
    send_time_utc = models.SmallIntegerField(null=True)
    response_type = models.SmallIntegerField()
    # 0 = Numeric
    # 1 = Binary
    # 2 = Text
    # 3 = File
    
class GoalEntry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    goal = models.ForeignKey(Goal)

    numeric_value = models.FloatField(null=True)
    binary_value = models.SmallIntegerField(null=True) # 0 = False, 1 = True
    text_value = models.CharField(max_length=1000, null=True)
    response_collected = models.SmallIntegerField(default=0)

class ToDoTask(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    text = models.CharField(max_length=300)

    completed = models.BooleanField(default=False)

class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    sent_to_user = models.BooleanField() # If false, then the message was sent from the user
    message_type = models.SmallIntegerField() # Message types are enumerated in message_log.py

    text = models.CharField(max_length=200, null=True)

    goal_in_reference = models.ForeignKey(Goal, null=True)







