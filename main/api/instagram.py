import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime

def refresh_instagram_history(user):
    x = 1