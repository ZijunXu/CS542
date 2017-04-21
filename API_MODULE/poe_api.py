from pymongo import MongoClient
import requests
import json
import os
import time
import re


class get_data_api:
    def __init__(self):
        # get the user id from last api query
        self.user_id = self.get_last_user_id()
        # create the folder for storing the data
        if not os.path.exists(os.getcwd() + '/data/'):
            os.makedirs(os.getcwd() + '/data')

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
            json.dump({"last_user": data}, outfile)

    def get_api_response(self):
        # we only store the items that have price note
        api_url = "http://api.pathofexile.com/public-stash-tabs/?id="
        r = requests.get(api_url + self.user_id)
        data = r.json()
        while 'next_change_id' not in data:
            r = requests.get(api_url + self.user_id)
            data = r.json()
            print("==================")
            print("Sleep for 1 minute")
            print("==================")
            time.sleep(60)
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
                        # set the value into int
                        if 'requirements' in item:
                            temp_req = {}
                            for req in item['requirements']:
                                req['values'] = int(req['values'][0][0])
                                temp_req[req['name']] = req['values']
                            item['requirements'] = temp_req

                        # set the value into float
                        if 'properties' in item:
                            temp_prop = {}
                            for prop in item['properties']:
                                if len(prop['values']) >= 1:
                                    if "%" in prop['values'][0][0]:
                                        prop['values'] = float(prop['values'][0][0][:-1])
                                        temp_prop[prop['name']] = prop['values']
                                    elif "-" in prop['values'][0][0]:
                                        atk = [float(n) for n in prop['values'][0][0].split('-')]
                                        prop['values'] = sum(atk) / len(atk)
                                        temp_prop[prop['name']] = prop['values']
                                    else:
                                        try:
                                            prop['values'] = float(prop['values'][0][0])
                                            temp_prop[prop['name']] = prop['values']
                                        except:
                                            prop['values'] = prop['values'][0][0]
                                            temp_prop[prop['name']] = prop['values']
                            item['properties'] = temp_prop

                        # set the socket into the format that we actually want
                        if 'sockets' in item:
                            group = {}
                            socket = 0
                            D = 0
                            S = 0
                            I = 0
                            other = 0
                            group_ans = []
                            for n in item['sockets']:
                                socket += 1
                                if n['group'] in group:
                                    group[n['group']] += 1
                                else:
                                    group[n['group']] = 1
                                group_ans = [count_link[1] for count_link in group.items()]
                                if n['attr'] == 'D':
                                    D += 1
                                elif n['attr'] == 'S':
                                    S += 1
                                elif n['attr'] == 'I':
                                    I += 1
                                else:
                                    other += 1
                            item['sockets'] = {'link': group_ans, 'socket_number': socket, 'D': D, 'S': S, 'I': I, 'Other': 0}

                        # parsing the mods
                        temp_mods = {}
                        if 'implicitMods' in item:
                            for n in item['implicitMods']:
                                temp_number = re.findall("\d+\.*\d*", n)
                                temp_string = re.sub("\d+\.*\d*","X",n)
                                if len(temp_number) == 0:
                                    temp_mods[temp_string] = 1
                                else:
                                    temp_mods[temp_string] = float(temp_number[0])
                            item.pop('implicitMods', None)

                        if 'craftedMods' in item:
                            for n in item['craftedMods']:
                                temp_number = re.findall("\d+\.*\d*", n)
                                temp_string = re.sub("\d+\.*\d*","X",n)
                                if len(temp_number) == 0:
                                    temp_mods[temp_string] = 1
                                else:
                                    temp_mods[temp_string] = float(temp_number[0])
                            item.pop('craftedMods', None)

                        if 'explicitMods' in item:
                            for n in item['explicitMods']:
                                temp_number = re.findall("\d+\.*\d*", n)
                                temp_string = re.sub("\d+\.*\d*","X",n)
                                if len(temp_number) == 0:
                                    temp_mods[temp_string] = 1
                                else:
                                    temp_mods[temp_string] = float(temp_number[0])
                            item.pop('explicitMods', None)

                        item['Mods'] = temp_mods
                        temp.append(item)

        if len(temp) != 0:
            client = MongoClient('mongodb://localhost:27017/')
            db = client.project_542
            posts = db.posts
            posts.insert_many(temp)
            print('Now MongoDB has %8i documents' % posts.count())
            print("==================")

        self.record_last_user_id(file_name)
        self.user_id = file_name
        # for n in temp:
        #    with open(os.getcwd() + '/data/' + self.user_id + '.json', 'a') as outfile:
        #        json.dump(n, outfile, indent=2)


if __name__ == "__main__":
    # notice, if we try too many times, the server will reject our request then reponed nothing
    print("Start the script")
    a = get_data_api()
    times = 1
    while times != 0:
        a.get_api_response()
