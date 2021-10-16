import requests
# from datetime import date, datetime
# from dateutil.relativedelta import relativedelta
# import math

# MongoDB connection
from pymongo import MongoClient

# Helpers
from read_csv import CSV

cluster = MongoClient("mongodb+srv://jinkim:SJsknyu774!@gait.my1fw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster['gait-sessions']
sessions = database['sessions']

get_token_url = 'https://api.runscribe.com/v2/authenticate'
get_runs_url = 'https://api.runscribe.com/v2/runs'

def main():
    body1 = {
        "email": "rs6418@nyu.edu",
        "password": "WallW25?"
    }

    res = requests.post(get_token_url, data=body1)

    token = res.json()["token"]

    # TODO: Check if header is required to get CSV files
    header = {
        "X-Auth-Token": token
    }

    res2 = requests.get(get_runs_url, headers=header)

    left_serial = []
    right_serial = []

    sessions = len(res2.json()["runs"])

    for i in range(sessions):
        curr_session = res2.json()["runs"][i]
        curr_location = curr_session["location"]

        left_serial.append(curr_location + "/" + curr_session['run_files'][1]['serial'] + ".csv")
        right_serial.append(curr_location + "/" + curr_session['run_files'][0]['serial'] + ".csv")

    res3 = requests.get(left_serial[0], headers=header)

    print(res3)


if __name__ == "__main__":
    main()