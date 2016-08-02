from django.core.management.base import BaseCommand, CommandError
from main.models import *
from main import messenger_helper

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        all_goals = Goal.objects.all()

        for g in all_goals:
            print('SENDING')
            print(g.name)