import requests

# MongoDB connection
from pymongo import MongoClient
import csv

CLUSTER = MongoClient("mongodb+srv://jinkim:SJsknyu774!@gait.my1fw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
DATABASE = CLUSTER['gait-sessions']
SESSIONS = DATABASE['sessions']

get_token_url = 'https://api.runscribe.com/v2/authenticate'
get_runs_url = 'https://api.runscribe.com/v2/runs'


def fill(res, features_ind, rows, dir, id):
    '''
    Processes the data from the rows into a more usable form (see below)

    res -> The data structure we want to add features to
    features_ind -> The dictionary that converts the respective indice with its feature
    row -> Data to process
    dir -> The direction of the 
    id -> ID of the session

    returns (res, features_ind)
    '''
    i = 0
    for feature in rows[0]:
        res[id][dir][feature] = []
        features_ind[i] = feature
        i += 1

    for i in range(1, len(rows)):
        row = rows[i]

        for j in range(len(row)):
            if (row[j] == ''): # If no data -> Skip and continue
                continue
            res[id][dir][features_ind[j]].append(float(row[j]))

    # Have to recalculate the "stride_length" feature because the sensor does not work properly
    a = res[id][dir]["stride_pace"]
    b = res[id][dir]["step_rate"]

    stride_updated = []

    # Formula for stride length
    # res = (a * 60 * 2) / b

    for i in range(len(a)):
        stride_updated.append((a[i] * 120) / b[i])

    res[id][dir]["stride_length"] = stride_updated

    return (res, features_ind)


def add_sessions_to_database(res):
    '''
    Adds all sessions to the database that are not already in the MongoDB collection
    NOTE: We do a pre check using check_database() so all the processed results have to
    go into the database
    '''
    cnt = 0

    for _id in res:
        # Adding ID to the body of the object
        res[_id]["_id"] = _id

        try:
            SESSIONS.insert_one(res[_id])
        except Exception as e:
            print("Something went wrong")
            print(e)

        cnt += 1

    if cnt == 0:
        return False, 0

    return True, cnt


def check_database():
    '''
    Checks to see which IDs are already in the database, so we don't process the ones that
    are already added
    '''
    tracked_sessions = set()

    for session in SESSIONS.find():
        _id = session["_id"] # The index of the database
        tracked_sessions.add(_id)

    return tracked_sessions


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

    curr_sessions_tracked = check_database()

    for i in range(sessions):
        curr_session = res2.json()["runs"][i]
        curr_location = curr_session["location"]

        # print(curr_location + "/mountings/" + curr_session['run_files'][0]['serial'] + ".csv")

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

        # Left side first
        # (url, id)
        CSV_URL = left_serial[i][0]
        SESSION_ID = left_serial[i][1]

        # We have already accounted for this session in the database
        if (SESSION_ID in curr_sessions_tracked):
            continue

        res[SESSION_ID] = {
            "left": {},
            "right": {}
        }

        features_ind = {}

        with requests.Session() as s:
            download = s.get(CSV_URL, headers=header)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            rows = list(cr)

            res, features_ind = fill(res, features_ind, rows, "left", SESSION_ID)

        # Moving onto the right side for that session
        features_ind = {}
        CSV_URL = right_serial[i][0]

        with requests.Session() as s:
            download = s.get(CSV_URL, headers=header)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            rows = list(cr)

            res, features_ind = fill(res, features_ind, rows, "right", SESSION_ID)

    # Now adding the sessions to the database
    success, added = add_sessions_to_database(res)

    # Sanity check after sessions are added
    if success:
        print(str(added) + " new sessions added")
    else:
        print("No new sessions detected")


if __name__ == "__main__":
    main()