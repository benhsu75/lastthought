import requests
from main.utils import constants
from requests.auth import HTTPBasicAuth
from main.models import *
import datetime
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
    base_datetime = datetime.datetime(year=2012, month=1, day=1)
    base_date_string = base_datetime.strftime('%Y-%m-%d');
    today_datetime = datetime.datetime.now()
    period = '1m'
    url_to_get = 'https://api.fitbit.com/1/user/{}/body/log/weight/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, base_date_string, period)

    while base_datetime.date() <= today_datetime.date():
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
                    weight_log_entry = WeightLogEntry(log=user_log, source_type=0, source_id=logId, metric_weight=metric_weight)

                    # Get datetime from date and time and set it
                    occurred_at = get_datetime_from_date_and_time(date, time)
                    weight_log_entry.occurred_at = occurred_at

                    weight_log_entry.save()
        else:
            # ERROR
            # TODO
            x = 1

        # Increment base_datetime
        base_datetime += relativedelta(months=1)
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

    if 'activities-log-steps' in r_steps.json():
        steps_list = r_steps.json()['activities-log-steps']

        for steps_log in steps_list:
            date = steps_log['dateTime']
            num_steps = steps_log['value']

            print "Steps Log: " + str(num_steps) + " Date: "  + date

    else:
        # ERROR
        print r_steps.text
        # TODO
        x = 1

    distance_url_to_get = 'https://api.fitbit.com/1/user/{}/{}/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, ACTIVITY_DISTANCE_PATH, "today", period)

    # while base_datetime.date() <= today_datetime.date():
    print 'Making Request to: ' + distance_url_to_get

    r_distance = requests.get(distance_url_to_get, headers=headers)

    # print r_distance.text

    if 'activities-log-distance' in r_distance.json():
        distance_list = r_distance.json()['activities-log-distance']

        for distance_log in distance_list:
            date = distance_log['dateTime']
            num_distance = distance_log['value']

            print "Distance Log: " + str(num_distance) + " Date: "  + date

    else:
        # ERROR
        print r_distance.text
        # TODO
        x = 1

    calories_url_to_get = 'https://api.fitbit.com/1/user/{}/{}/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, ACTIVITY_CALORIES_PATH, "today", period)

    # while base_datetime.date() <= today_datetime.date():
    print 'Making Request to: ' + calories_url_to_get

    r_calories = requests.get(calories_url_to_get, headers=headers)

    # print r_calories.text

    if 'activities-log-calories' in r_calories.json():
        calories_list = r_calories.json()['activities-log-calories']

        for calories_log in calories_list:
            date = calories_log['dateTime']
            num_calories = calories_log['value']

            print "Calories Log: " + str(num_calories) + " Date: "  + date

    else:
        # ERROR
        print r_calories.text
        # TODO
        x = 1


# def refresh_sleep_history(user, access_token=None):
#     # Get the access token
#     if not access_token:
#         access_token = refresh_bearer_token(user)

#     # Make request
#     user_log = Log.find_or_create(user)
    
#     # Make request to /ride
#     headers = {
#         'Authorization' : 'Bearer ' + access_token
#     }

#     # Loop through requests to get weight
#     more_to_parse = True
#     base_datetime = datetime.datetime(year=2010, month=1, day=1)
#     base_date_string = base_datetime.strftime('%Y-%m-%d');
#     today_datetime = datetime.datetime.now()
#     period = '1m'
#     url_to_get = 'https://api.fitbit.com/1/user/{}/body/log/activities/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, base_date_string, period)

#     while base_datetime.date() <= today_datetime.date():
#         print 'Making Request to: ' + url_to_get
#         r = requests.get(url_to_get, headers=headers)

#         if 'weight' in r.json():
#             weight_list = r.json()['weight']

#             for weight_log in weight_list:
#                 date = weight_log['date']
#                 time = weight_log['time']
#                 logId = weight_log['logId']
#                 metric_weight = weight_log['metric_weight']
#                 source = weight_log['source']

#                 print "Weight Log: " + str(metric_weight)
                
#                 weight_log_entry = WeightLogEntry.objects.get(log=user_log)

#         else:
#             # ERROR
#             # TODO
#             x = 1

#         # Increment base_datetime
#         base_datetime += relativedelta(months=1)
#         base_date_string = base_datetime.strftime('%Y-%m-%d');
#         url_to_get = 'https://api.fitbit.com/1/user/{}/body/log/weight/date/{}/{}.json'.format(user.fitbitconnection.fitbit_id, base_date_string, period)

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
