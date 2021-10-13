import requests

'''
Resources:
https://github.com/richardjy/read-runscribe

'''

get_token_url = 'https://api.runscribe.com/v2/authenticate'
get_runs_url = 'https://api.runscribe.com/v2/runs'

def main():
    body1 = {
        "email": "rs6418@nyu.edu",
        "password": "WallW25?"
    }

    res = requests.post(get_token_url, data=body1)

    token = res.json()["token"]

    # print(token)

    header = {
        "X-Auth-Token": token
    }

    res2 = requests.get(get_runs_url, headers=header)

    print(res2.json()["runs"])




if __name__ == "__main__":
    main()