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
    # {"requirements.Dex": {"$gte": form.min_requirements_dex.data,"$lt": form.max_requirements_dex.data}}
    # {"requirements.Dex": {"$gte": form.min_requirements_dex.data}}
    # {"requirements.Str": {"$gte": form.min_requirements_str.data,"$lt": form.max_requirements_str.data}}
    # {"requirements.Str": {"$gte": form.min_requirements_str.data}}
    # {"requirements.Level": {"$gte": form.min_requirements_lvl.data,"$lt": form.max_requirements_lvl.data}}
    # {"requirements.Level": {"$gte": form.min_requirements_lvl.data}}
    ans = posts.find({"requirements.Int": {"$gte": 1,
                                           "$lt": 100}})
    ans = posts.find({"requirements.Level": {"$gte": 1}})
    # {"properties.Physical Damage": {"$gte": form.physical_damage.data}}
    # {"properties.Elemental Damage": {"$gte": form.elemental_damage.data}}
    # {"properties.Critical Strike Chance": {"$gte": form.min_critical_strike_chance.data, "$lt": form.max_critical_strike_chance.data}}
    # {"properties.Critical Strike Chance": {"$gte": form.min_critical_strike_chance.data}}
    # {"properties.Attacks per Second": {"$gte": form.min_attacks_per_second.data,"$lt": form.max_attacks_per_second.data}}
    # {"properties.Attacks per Second": {"$gte": form.min_attacks_per_second.data}}
    # {"properties.Armour": {"$gte": form.min_armour.data,"$lt": form.max_armour.data}}
    # {"properties.Armour": {"$gte": form.min_armour.data}}
    # {"properties.Evasion Rating": {"$gte": form.min_evasion.data,"$lt": form.max_evasion.data}}
    # {"properties.Evasion Rating": {"$gte": form.min_evasion.data}}
    # {"properties.Energy Shield": {"$gte": form.min_shield.data, "$lt": form.max_shield.data}}
    # {"properties.Energy Shield": {"$gte": form.min_shield.data}}
    ans = posts.find({"properties.Physical Damage": {"$gte": 10}})

    # {"Mods.X% increased Attack Speed": {"$gte": form.Mods.data}}
    ans = posts.find({"Mods.X% increased Attack Speed": {"$gte": 3}})

    # {"Price.Currency": form.currency_name.data, "Price.Number":}
    ans = posts.find({"Price.Currency": 'chaos', "Price.Number": {"$gte": 1, "$lt": 5}})
    print(ans.count(), "=====")
    ans = posts.find({"$and": [{"corrupted": False},
                               {"league": "Standard"},
                               {"identified": True},
                               {"verified": False},
                               {"ilvl": {"$gte": 10, "$lt": 60}},
                               {"sockets.socket_number": {"$gte": 0, "$lt": 6}},
                               {"sockets.link": 1},
                               {"sockets.S": {"$gte": 1}},
                               {"requirements.Int": {"$gte": 1,
                                                     "$lt": 100}},
                               ]})
    print(ans.count())

    # {"name": form.name.data}
    # {"typeLine": form.typeLine.data}
