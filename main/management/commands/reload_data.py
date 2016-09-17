from django.core.management.base import BaseCommand, CommandError
from main.models import *
from datetime import datetime
import json
from main.api import lyft, uber, instagram, foursquare, fitbit

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        all_users = User.objects.all()

        for user in all_users:
            # # Refresh lyft
            # if hasattr(user,'lyftconnection'):
            #     lyft.refresh_ride_history(user)

            # # Refresh uber
            # if hasattr(user,'uberconnection'):
            #     uber.refresh_ride_history(user)

            # Refresh foursquare
            if hasattr(user,'foursquareconnection'):
                foursquare.refresh_checkin_history(user)

            # # Refresh instagram
            # if hasattr(user,'instagramconnection'):
            #     instagram.refresh_instagram_history(user)