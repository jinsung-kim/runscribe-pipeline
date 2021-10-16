import requests

# MongoDB connection
from pymongo import MongoClient

# Helpers
import csv

cluster = MongoClient("mongodb+srv://jinkim:SJsknyu774!@gait.my1fw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster['gait-sessions']
sessions = database['sessions']

get_token_url = 'https://api.runscribe.com/v2/authenticate'
get_runs_url = 'https://api.runscribe.com/v2/runs'

def main():
    # Login information
    body1 = {
        "email": "rs6418@nyu.edu",
        "password": "WallW25?"
    }

    # Getting authentication token
    res = requests.post(get_token_url, data=body1)

    token = res.json()["token"]

    # This is required to get any information from the API
    header = {
        "X-Auth-Token": token
    }

    res2 = requests.get(get_runs_url, headers=header)

    # Used to store all of the URLs + IDs that we need to check
    left_serial = []
    right_serial = []

    sessions = len(res2.json()["runs"])

    for i in range(sessions):
        curr_session = res2.json()["runs"][i]
        curr_location = curr_session["location"]

        left_serial.append((curr_location + "/mountings/" + curr_session['run_files'][1]['serial'] + ".csv", curr_session["id"]))
        right_serial.append((curr_location + "/mountings/" + curr_session['run_files'][0]['serial'] + ".csv", curr_session["id"]))

    '''
    This is where the left and right objects will be stored by session ID

    res = {
        380554: { ID is key for dictionary
            "left": {
                "step_rate": [],
                "step_length": [],
                "stride_pace": []
            },
            "right": {
                "step_rate": [],
                "step_length": [],
                "stride_pace": []
            }
        }
    }
    '''
    res = {}

    # For each of the serial links -> Calculate the values
    for i in range(len(left_serial)):
        if i == 1:
            break

        # left_csv = requests.get(left_serial[i], headers=header) # .content.decode('utf-8')
        # right_csv = CSV("r", requests.get(right_serial[i], headers=header)) # .content.decode('utf-8')

        # (url, id)
        CSV_URL = left_serial[i][0]
        SESSION_ID = left_serial[i][1]

        res[SESSION_ID] = {
            "left": {},
            "right": {}
        }

        feature_ind = {}

        # Left side first
        with requests.Session() as s:
            download = s.get(CSV_URL, headers=header)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            rows = list(cr)

            # First row will be the features that are being traced
            i = 0
            for feature in rows[0]:
                res[SESSION_ID]["left"][feature] = []
                feature_ind[i] = feature
                i += 1

            for i in range(1, len(rows)):
                row = rows[i]

                for j in range(len(row)):
                    res[SESSION_ID]["left"][feature_ind[j]].append(float(row[j]))

        print(res)
        
        # CSV_URL = right_serial[i][0]
        # with requests.Session() as s:
        #     download = s.get(CSV_URL, headers=header)

        #     decoded_content = download.content.decode('utf-8')

        #     cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        #     rows = list(cr)

        #     header_row = True
        #     for row in rows:
        #         if header_row: # This contains the header row
        #             pass
        #         else:
        #             pass


if __name__ == "__main__":
    main()