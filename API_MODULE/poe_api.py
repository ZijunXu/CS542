import requests
import json
import os
import time


class get_data_api:
    def __init__(self):
        # get the user id from last api query
        self.user_id = self.get_last_user_id()
        # create the folder for storing the data
        if not os.path.exists(os.getcwd()+'/data/'):
            os.makedirs(os.getcwd()+'/data')

    def get_last_user_id(self):
        # set the last user id
        for file_name in os.listdir():
            if file_name == 'last_user.json':
                with open('last_user.json') as json_data:
                    data = json.load(json_data)
                return str(data["last_user"])
        return "0"

    def record_last_user_id(self, data):
        # record the user id
        with open('last_user.json', 'w') as outfile:
            json.dump({"last_user":data}, outfile)

    def get_api_response(self):
        # we only store the items that have price note
        api_url = "http://api.pathofexile.com/public-stash-tabs/?id="
        r = requests.get(api_url+self.user_id)
        data = r.json()
        file_name = data['next_change_id']
        print("Current id: ", self.user_id + " next id: ", file_name)
        temp = []
        for account in data['stashes']:
            # player with public stashes and has items
            if account['public'] != False and len(account['items']) != 0:
                # items has note
                for item in account['items']:
                    if 'note' in item:
                        item['owner'] = account['accountName']
                        temp.append(item)
        if len(temp) != 0:
            with open(os.getcwd() + '/data/'+self.user_id+'.json', 'a') as outfile:
                json.dump(temp, outfile, indent=2)
        self.record_last_user_id(file_name)
        self.user_id = file_name

if __name__ == "__main__":
    # notice, if we try too many times, the server will reject our request then reponed nothing
    print("Start the script")
    a = get_data_api()
    times = 1
    while times != 0:
        a.get_api_response()

