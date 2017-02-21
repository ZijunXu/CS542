import requests
import json
import os

class get_data_api:
    def __init__(self):
        self.user_id = self.get_last_user_id()
        if not os.path.exists(os.getcwd()+'/data/'):
            os.makedirs(os.getcwd()+'/data')

    def get_last_user_id(self):
        for file_name in os.listdir():
            if file_name == 'last_user.json':
                with open('last_user.json') as json_data:
                    data = json.load(json_data)
                return str(data["last_user"])

        return "0"

    def record_last_user_id(self, data):
        with open('last_user.json', 'w') as outfile:
            json.dump({"last_user":data}, outfile)

    def get_api_response(self):
        api_url = "http://api.pathofexile.com/public-stash-tabs/?id="
        print(self.user_id)
        r = requests.get(api_url+self.user_id)
        data = r.json()
        file_name = data['next_change_id']
        self.record_last_user_id(file_name)
        temp = []
        for account in data['stashes']:
            # player with public stashes and has items
            if account['public'] != False and len(account['items']) != 0:
                # items has note
                for item in account['items']:
                    if 'note' in item:
                        item['owner'] = account['accountName']
                        #print(json.dumps(item))
                        temp.append(item)
        with open(os.getcwd() + '/data/'+file_name+'.json', 'a') as outfile:
            json.dump(temp, outfile)
