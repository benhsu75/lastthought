from django.db import models

class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fbid = models.CharField(max_length=200)
    state = models.SmallIntegerField()
    full_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)

    active_habit_entry = models.ForeignKey('HabitEntry', default=None, null=True)

# Represents known information about the user
class BackgroundInformation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    current_zip_code = models.CharField(max_length=10, null=True)

    user = models.OneToOneField(User)

# User States
# 0 - Onboarding after initial messages
# 1 - Neutral state
