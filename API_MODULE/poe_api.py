import requests
import json

api_url = "http://api.pathofexile.com/public-stash-tabs/?id="
user_id = "0"
r = requests.get(api_url+user_id)
data = r.json()



# next change id for the api query
print(data['next_change_id'])


for account in data['stashes']:
    # player with public stashes and has items
    if account['public'] != False and len(account['items']) != 0:
        # items has note
        for item in account['items']:
            if 'note' in item:
                print(item['note'])
