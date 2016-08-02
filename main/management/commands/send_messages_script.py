from django.core.management.base import BaseCommand, CommandError
from main.models import *

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print("EXECUTING COMMAND")