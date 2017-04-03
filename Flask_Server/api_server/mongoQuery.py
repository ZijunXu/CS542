from pymongo import MongoClient
import pprint

client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')

db = client.project_542
'''all data are stored in the posts collection of the project_542 database'''
posts = db.posts
for post in posts.find({"$and": [{'ilvl':  {"$gte": 39, "$lt": 42}}, {'corrupted': False},
                                 {'explicitMods': {"$all": ['10% increased Damage', '12% increased Area Damage']}}]}):
    pprint.pprint(post)

# for post in posts.find({"$allnd": [{'ilvl':  {"$gte": 39, "$lt": 42}}, {'corrupted': False},
#                                  {'explicitMods': '10% increased Damage'}, {'explicitModes': '12% increased Area Damage'},
#                                  {'name': '<<set:MS>><<set:M>><<set:S>>Rapture Splinter'}]}):
#     pprint.pprint(post)