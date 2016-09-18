import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime, pytz
from dateutil.relativedelta import relativedelta

def refresh_bearer_token(user):
    # Get refresh token
    refresh_token = user.fitbitconnection.refresh_token

    # Make request to get access_token
    payload = {
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token
    }

    OAUTH_URL = 'https://api.fitbit.com/oauth2/token'

    r = requests.post(OAUTH_URL, data=payload, auth=HTTPBasicAuth(constants.FITBIT_CLIENT_ID, constants.FITBIT_CLIENT_SECRET));

    print r.text

    bearer_token = r.json()['access_token']
    refresh_token = r.json()['refresh_token']

    user.fitbitconnection.refresh_token = refresh_token
    user.fitbitconnection.save()

    return bearer_token


def refresh_weight_history(user, access_token=None):
    # Get the access token
    if not access_token:
        access_token = refresh_bearer_token(user)

    # Make request
    user_log = Log.find_or_create(user)
    
    # Make request to /ride
    headers = {
        'Authorization' : 'Bearer ' + access_token
    }

    # Loop through requests to get weight
    months_to_go_back = 12
    base_datetime = datetime.datetime.now()
    # base_datetime -= relativedelta(months=1) # Go 1 month back first
    base_date_string = base_datetime.strftime('%Y-%m-%d');
    period = '1m'
    url_to_get = 'https://api.fitbit.com/1/user/{}/body/log/weight/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, base_date_string, period)

    for x in range(0,months_to_go_back):
        print 'Making Request to: ' + url_to_get
        r = requests.get(url_to_get, headers=headers)

        print r.text

        if 'weight' in r.json():
            weight_list = r.json()['weight']

            for weight_log in weight_list:
                date = weight_log['date']
                time = weight_log['time']
                logId = weight_log['logId']
                metric_weight = weight_log['weight']

                print "Weight Log: " + str(metric_weight)
                
                try:
                    weight_log_entry = WeightLogEntry.objects.get(log=user_log, source_id=logId)
                except WeightLogEntry.DoesNotExist:

                    # Get datetime from date and time and set it
                    occurred_at = get_datetime_from_date_and_time(date, time)

                    weight_log_entry = WeightLogEntry(log=user_log, source_type=0, source_id=logId, metric_weight=metric_weight, entry_type=6, occurred_at=occurred_at)

                    weight_log_entry.save()
        else:
            # ERROR
            # TODO
            x = 1

        # Increment base_datetime
        base_datetime -= relativedelta(months=1)
        base_date_string = base_datetime.strftime('%Y-%m-%d');
        url_to_get = 'https://api.fitbit.com/1/user/{}/body/log/weight/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, base_date_string, period)

ACTIVITY_STEPS_PATH = 'activities/steps'
ACTIVITY_DISTANCE_PATH = 'activities/distance'
ACTIVITY_CALORIES_PATH = 'activities/calories'

def refresh_activity_history(user, access_token=None):
    # Get the access token
    if not access_token:
        access_token = refresh_bearer_token(user)

    # Make request
    user_log = Log.find_or_create(user)
    
    # Make request to /ride
    headers = {
        'Authorization' : 'Bearer ' + access_token
    }

    # Get all steps data
    period = 'max'
    steps_url_to_get = 'https://api.fitbit.com/1/user/{}/{}/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, ACTIVITY_STEPS_PATH, "today", period)

    # while base_datetime.date() <= today_datetime.date():
    print 'Making Request to: ' + steps_url_to_get

    r_steps = requests.get(steps_url_to_get, headers=headers)

    # print r_steps.text

    retrieved_steps = False
    retrieved_distance = False
    retrieved_calories = False

    steps_list = []
    distance_list = []
    calories_list = []

    if 'activities-steps' in r_steps.json():
        retrieved_steps = True
        steps_list = r_steps.json()['activities-steps']
    else:
        # ERROR
        print r_steps.text

    distance_url_to_get = 'https://api.fitbit.com/1/user/{}/{}/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, ACTIVITY_DISTANCE_PATH, "today", period)

    # while base_datetime.date() <= today_datetime.date():
    print 'Making Request to: ' + distance_url_to_get

    r_distance = requests.get(distance_url_to_get, headers=headers)

    if 'activities-distance' in r_distance.json():
        retrieved_distance = True
        distance_list = r_distance.json()['activities-distance']
    else:
        # ERROR
        print r_distance.text

    calories_url_to_get = 'https://api.fitbit.com/1/user/{}/{}/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, ACTIVITY_CALORIES_PATH, "today", period)

    # while base_datetime.date() <= today_datetime.date():
    print 'Making Request to: ' + calories_url_to_get

    r_calories = requests.get(calories_url_to_get, headers=headers)

    if 'activities-calories' in r_calories.json():
        calories_list = r_calories.json()['activities-calories']
        retrieved_calories = True
    else:
        # ERROR
        print r_calories.text

    # Confirm that the length of steps, calories, and distance list is the same
    if len(steps_list) != len(distance_list) or len(distance_list) != len(calories_list):
        # Error
        print 'ERROR - LIST SIZES DO NOT MATCH'

    # Create activity log entries
    if retrieved_calories and retrieved_steps and retrieved_distance:
        # Loop through the data
        for x in range(0, len(steps_list)):
            # Extract information
            steps = steps_list[x]
            distance = distance_list[x]
            calories = calories_list[x]

            steps_date = steps['dateTime']
            distance_date = distance['dateTime']
            calories_date = distance['dateTime']

            num_steps = steps['value']
            num_distance = distance['value']
            num_calories = calories['value']

            # Confirm that the dateTimes are equal
            if steps_date != distance_date or distance_date != calories_date:
                # Error
                print "dateTimes ARE NOT MATCHING UP"

            num_steps_int = int(num_steps)
            num_distance_float = float(num_distance)
            num_calories_int = int(num_calories)

            # Convert dateTime to datetime
            occurred_at_datetime = datetime.datetime.strptime(steps_date, '%Y-%m-%d').replace(hour=0, minute=0, second=0, tzinfo=pytz.UTC)

            # Check if activity_log_entry exists yet for that date
            try:
                activity_log_entry = ActivityLogEntry.objects.get(occurred_at=occurred_at_datetime)
            except ActivityLogEntry.DoesNotExist:   
                # Instantiate model object
                activity_log_entry = ActivityLogEntry(source_type=0, num_steps=num_calories_int, distance_km=num_distance_float, num_calories=num_calories_int, occurred_at=occurred_at_datetime, entry_type=7, log=user_log)
                activity_log_entry.save()

        print 'Created ' + str(len(steps_list)) + " Activity log entries!"

def refresh_sleep_history(user, access_token=None):
    # Get the access token
    if not access_token:
        access_token = refresh_bearer_token(user)

    # Make request
    user_log = Log.find_or_create(user)
    
    # Make request to /ride
    headers = {
        'Authorization' : 'Bearer ' + access_token
    }

    # Loop through requests to get weight
    more_to_parse = True
    base_datetime = datetime.datetime(year=2010, month=1, day=1)
    base_date_string = base_datetime.strftime('%Y-%m-%d');
    today_datetime = datetime.datetime.now()
    period = '1m'
    url_to_get = 'https://api.fitbit.com/1/user/{}/body/log/activities/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, base_date_string, period)

    while base_datetime.date() <= today_datetime.date():
        print 'Making Request to: ' + url_to_get
        r = requests.get(url_to_get, headers=headers)

        if 'weight' in r.json():
            weight_list = r.json()['weight']

            for weight_log in weight_list:
                date = weight_log['date']
                time = weight_log['time']
                logId = weight_log['logId']
                metric_weight = weight_log['metric_weight']
                source = weight_log['source']

                print "Weight Log: " + str(metric_weight)
                
                weight_log_entry = WeightLogEntry.objects.get(log=user_log)

        else:
            # ERROR
            # TODO
            x = 1

        # Increment base_datetime
        base_datetime += relativedelta(months=1)
        base_date_string = base_datetime.strftime('%Y-%m-%d');
        url_to_get = 'https://api.fitbit.com/1/user/{}/body/log/weight/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, base_date_string, period)

def get_profile_information(user, access_token):
    url_to_get = 'https://api.fitbit.com/1/user/'+user.fitbitconnection.fitbit_id+'/profile.json'

    headers = {
        'Authorization' : 'Bearer ' + access_token
    }

    r = requests.get(url_to_get, headers=headers)

    print r.text

    return r.json()

# HELPER METHODS

def get_datetime_from_date_and_time(date, time):
    date_time_combined = date + ' ' + time
    occurred_at = datetime.datetime.strptime(date_time_combined, '%Y-%m-%d %H:%M:%S')
    return occurred_at
