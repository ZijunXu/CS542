from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    db = client.project_542
    posts = db.posts
    # {"league": form.league.data}
    ans = posts.find({"league": "Standard"})
    # {"corrupted": form.corrupted.data}
    ans = posts.find({"corrupted": True})
    # {"verified": form.verified.data}
    ans = posts.find({"verified": False})
    # {"identified": form.identified.data}
    ans = posts.find({"identified": True})
    # {"ilvl": {"$gte": form.min_ilvl.data, "$lt": form.max_ilvl.data}}
    # {"ilvl": {"$gte": form.min_ilvl.data}}
    ans = posts.find({"ilvl": {"$gte": 10, "$lt": 60}})
    # {"sockets.socket_number": {"$gte": form.min_socket_number.data,"$lt": form.max_socket_number.data}}
    # {"sockets.socket_number": {"$gte": form.min_socket_number.data}}
    ans = posts.find({"sockets.socket_number": {"$gte": 0, "$lt": 6}})
    # {"sockets.link": form.max_link_number.data}
    # {"sockets.link": form.min_link_number.data}
    ans = posts.find({"sockets.link": 1})
    # {"sockets.S": {"$gte": form.min_str_socket.data}}
    # {"sockets.D": {"$gte": form.min_dex_socket.data}}
    # {"sockets.I": {"$gte": form.min_int_socket.data}}
    # {"sockets.Other": {"$gte": form.min_other_socket.data}}
    ans = posts.find({"sockets.S": {"$gte": 1}})
    # {"requirements.name": "Dex", "requirements.values": {"$gte": form.min_requirements_dex.data,"$lt": form.max_requirements_dex.data}}
    # {"requirements.name": "Dex", "requirements.values": {"$gte": form.min_requirements_dex.data}}
    # {"requirements.name": "Str", "requirements.values": {"$gte": form.min_requirements_str.data,"$lt": form.max_requirements_str.data}}
    # {"requirements.name": "Str", "requirements.values": {"$gte": form.min_requirements_str.data}}
    # {"requirements.name": "Level", "requirements.values": {"$gte": form.min_requirements_lvl.data,"$lt": form.max_requirements_lvl.data}}
    # {"requirements.name": "Level", "requirements.values": {"$gte": form.min_requirements_lvl.data}}
    ans = posts.find({"requirements.name": "Int",
                      "requirements.values": {"$gte": 1,
                                              "$lt": 100}})
    ans = posts.find({"requirements.name": "Level",
                      "requirements.values": {"$gte": 1}})
    # {"properties.name": "Physical Damage", "properties.values": {"$gte": form.physical_damage.data}}
    # {"properties.name": "Elemental Damage","properties.values": {"$gte": form.elemental_damage.data}}
    # {"properties.name": "Critical Strike Chance","properties.values": {"$gte": form.min_critical_strike_chance.data, "$lt": form.max_critical_strike_chance.data}}
    # {"properties.name": "Critical Strike Chance", "properties.values": {"$gte": form.min_critical_strike_chance.data}}
    # {"properties.name": "Attacks per Second","properties.values": {"$gte": form.min_attacks_per_second.data,"$lt": form.max_attacks_per_second.data}}
    # {"properties.name": "Attacks per Second.data","properties.values": {"$gte": form.min_attacks_per_second.data}}
    # {"properties.name": "Armour","properties.values": {"$gte": form.min_armour.data,"$lt": form.max_armour.data}}
    # {"properties.name": "Armour", "properties.values": {"$gte": form.min_armour.data}}
    # {"properties.name": "Evasion Rating","properties.values": {"$gte": form.min_evasion.data,"$lt": form.max_evasion.data}}
    # {"properties.name": "Evasion Rating", "properties.values": {"$gte": form.min_evasion.data}}
    # {"properties.name": "Energy Shield","properties.values": {"$gte": form.min_shield.data, "$lt": form.max_shield.data}}
    # {"properties.name": "Energy Shield", "properties.values": {"$gte": form.min_shield.data}}
    ans = posts.find({"properties.name": "Physical Damage", "properties.values": {"$gte": 10}})
    print(ans.count())
    ans = posts.find({"$and": [{"corrupted": False},
                               {"league": "Standard"},
                               {"identified": True},
                               {"verified": False},
                               {"ilvl": {"$gte": 10, "$lt": 60}},
                               {"sockets.socket_number": {"$gte": 0, "$lt": 6}},
                               {"sockets.link": 1},
                               {"sockets.S": {"$gte": 1}},
                               {"requirements.name": "Int",
                                "requirements.values": {"$gte": 1,
                                                        "$lt": 100}},
                               ]})
    print(ans.count())

    # {"name": form.name.data}
    # {"typeLine": form.typeLine.data}


