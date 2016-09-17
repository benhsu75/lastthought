from django.core.management.base import BaseCommand, CommandError
from main.models import *
from datetime import datetime
import json
from main.api import *

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        all_users = User.objects.all()

        for user in all_users:
            # Refresh lyft
            
            # Refresh uber

            # Refresh