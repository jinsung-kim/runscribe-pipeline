import requests

'''
Resources:
https://github.com/richardjy/read-runscribe

'''

get_token_url = 'https://api.runscribe.com/v2/authenticate'
get_runs_url = 'https://api.runscribe.com/v2/runs'
get_csv_url = 'https://dashboard.runscribe.com/runs/{}/mountings/{}.csv'

def main():
    body1 = {
        "email": "rs6418@nyu.edu",
        "password": "WallW25?"
    }

    res = requests.post(get_token_url, data=body1)

    token = res.json()["token"]

    # print(token)

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
        # curr_id = curr_session["id"]
        curr_location = curr_session["location"]

        # print(curr_location)
        # print(curr_session['run_files'])
        left_serial.append(curr_location + "/" + curr_session['run_files'][1]['serial'] + ".csv")
        right_serial.append(curr_location + "/" + curr_session['run_files'][0]['serial'] + ".csv")

    # print(res2.json()["runs"][0])
    # print(left_serial)
    # print(right_serial)

    res3 = requests.get(left_serial[0], headers=header)

    print(res3)


if __name__ == "__main__":
    main()