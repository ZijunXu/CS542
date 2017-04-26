def parser(form):
    query_and = []
    price_name = {"Blessed Orb": "bless",
                  "Cartographer's Chisel": "chisel", "Chaos Orb": "chaos", "Chromatic Orb": "chrome",
                  "Divine Orb": "div", "Exalted Orb": "exa", "Gemcutter's Prism": "gem", "Jeweller's Orb": "jew",
                  "Orb of Alchemy": "alch", "Orb of Alteration": "alt", "Orb of Chance": "chance",
                  "Orb of Fusing": "fus", "Orb of Regret": "regret", "Orb of Scouring": "scour", "Regal Orb": "regal",
                  "Vaal Orb": "vaal", "Perandus Coin": "perandus", "Silver Coin": "silver"}

    if form.currency_name.data:
        if form.min_price.data:
            if form.max_price.data:
                query_and.append({"Price.Currency": price_name[form.currency_name.data],
                                  "Price.Number": {"$gte": form.min_price.data, "$lte": form.max_price.data}})
            else:
                query_and.append({"Price.Currency": price_name[form.currency_name.data],
                                  "Price.Number": {"$gte": form.min_price.data}})
        else:
            if form.max_price.data:
                query_and.append({"Price.Currency": price_name[form.currency_name.data],
                                  "Price.Number": {"$lte": form.max_price.data}})
            else:
                query_and.append({"Price.Currency": price_name[form.currency_name.data]})

    if form.name.data:
        query_and.append({"name": {"$regex":form.name.data, "$options":"gi"}})

    if form.type.data:
        if form.type.data == 'Flask' or form.type.data[-1] == 's':
            query_and.append({"type": form.type.data})
        else:
            query_and.append({"type": form.type.data.replace(" ","") + "s"})

    if form.typeLine.data:
        query_and.append({"typeLine": form.typeLine.data})

    if form.league.data:
        query_and.append({"league": form.league.data})

    if form.corrupted.data:
        query_and.append({"corrupted": form.corrupted.data})

    if form.verified.data:
        query_and.append({"verified": form.verified.data})

    if form.identified.data:
        query_and.append({"identified": form.identified.data})

    if form.min_ilvl.data:
        if form.max_ilvl.data:
            query_and.append({"ilvl": {"$gte": form.min_ilvl.data, "$lte": form.max_ilvl.data}})
        else:
            query_and.append({"ilvl": {"$gte": form.min_ilvl.data}})

    if form.min_socket_number.data:
        if form.max_socket_number.data:
            query_and.append({"sockets.socket_number": {"$gte": form.min_socket_number.data,
                                                        "$lte": form.max_socket_number.data}})
        else:
            query_and.append({"sockets.socket_number": {"$gte": form.min_socket_number.data}})

    if form.min_link_number.data:
        if form.max_link_number.data:
            query_and.append(
                {"sockets.link": {"$in": [i for i in range(form.min_link_number.data, form.min_link_number.data + 1)]}})
        else:
            query_and.append({"sockets.link": {"$in": [i for i in range(form.min_link_number.data, 7)]}})
    else:
        if form.max_link_number.data:
            query_and.append({"sockets.link": {"$in": [i for i in range(0, form.max_link_number.data)]}})

    if form.str_socket.data:
        query_and.append({"sockets.S": {"$gte": form.str_socket.data}})

    if form.dex_socket.data:
        query_and.append({"sockets.D": {"$gte": form.dex_socket.data}})

    if form.int_socket.data:
        query_and.append({"sockets.I": {"$gte": form.int_socket.data}})

    if form.other_socket.data:
        query_and.append({"sockets.Other": {"$gte": form.other_socket.data}})

    # requirements
    if form.min_requirements_int.data:
        if form.max_requirements_int.data:
            query_and.append(
                {"requirements.Int": {"$gte": form.min_requirements_int.data,
                                      "$lte": form.max_requirements_int.data}})
        else:
            query_and.append(
                {"requirements.Int": {"$gte": form.min_requirements_int.data}})
    else:
        if form.max_requirements_int.data:
            query_and.append(
                {"requirements.Int": {"$lte": form.max_requirements_int.data}})

    if form.min_requirements_dex.data:
        if form.max_requirements_dex.data:
            query_and.append(
                {"requirements.Dex": {"$gte": form.min_requirements_dex.data,
                                      "$lte": form.max_requirements_dex.data}})
        else:
            query_and.append(
                {"requirements.Dex": {"$gte": form.min_requirements_dex.data}})
    else:
        if form.max_requirements_dex.data:
            query_and.append(
                {"requirements.Dex": {"$lte": form.max_requirements_dex.data}})

    if form.min_requirements_str.data:
        if form.max_requirements_str.data:
            query_and.append(
                {"requirements.Str": {"$gte": form.min_requirements_str.data,
                                      "$lte": form.max_requirements_str.data}})
        else:
            query_and.append(
                {"requirements.Str": {"$gte": form.min_requirements_str.data}})
    else:
        if form.max_requirements_str.data:
            query_and.append(
                {"requirements.Str": {"$lte": form.max_requirements_str.data}})

    if form.min_requirements_lvl.data:
        if form.max_requirements_lvl.data:
            query_and.append(
                {"requirements.Level": {"$gte": form.min_requirements_lvl.data,
                                        "$lte": form.max_requirements_lvl.data}})
        else:
            query_and.append(
                {"requirements.Level": {"$gte": form.min_requirements_lvl.data}})
    else:
        if form.max_requirements_lvl.data:
            query_and.append(
                {"requirements.Level": {"$lte": form.max_requirements_lvl.data}})

    # properties
    if form.min_physical_damage.data:
        if form.max_physical_damage.data:
            damage = float(form.min_physical_damage.data) + float(form.max_physical_damage.data)
            query_and.append(
                {"properties.Physical Damage": {"$gte": damage / 2}})
        else:
            damage = float(form.min_physical_damage.data)
            query_and.append(
                {"properties.Physical Damage": {"$gte": damage}})
    else:
        if form.max_physical_damage.data:
            damage = float(form.max_physical_damage.data)
            query_and.append(
                {"properties.Physical Damage": {"$lte": damage}})

    if form.min_elemental_damage.data:
        if form.max_elemental_damage.data:
            edamage = float(form.min_elemental_damage.data) + float(form.max_elemental_damage.data)
            query_and.append(
                {"properties.Elemental Damage": {"$gte": edamage / 2}})
        else:
            edamage = float(form.min_elemental_damage.data)
            query_and.append(
                {"properties.Elemental Damage": {"$gte": edamage}})
    else:
        if form.max_elemental_damage.data:
            edamage = float(form.max_elemental_damage.data)
            query_and.append(
                {"properties.Elemental Damage": {"$lte": edamage}})

    if form.min_critical_strike_chance.data:
        if form.max_critical_strike_chance.data:
            crit = float(form.min_critical_strike_chance.data) + float(form.max_critical_strike_chance.data)
            query_and.append(
                {"properties.Critical Strike Chance": {"$gte": crit / 2}})
        else:
            crit = float(form.min_critical_strike_chance.data)
            query_and.append(
                {"properties.Critical Strike Chance": {"$gte": crit}})
    else:
        if form.max_critical_strike_chance.data:
            crit = float(form.max_critical_strike_chance.data)
            query_and.append(
                {"properties.Critical Strike Chance": {"$lte": crit}})

    if form.min_attacks_per_second.data:
        if form.max_attacks_per_second.data:
            aps = float(form.min_attacks_per_second.data) + float(form.max_attacks_per_second.data)
            query_and.append(
                {"properties.Attacks per Second": {"$gte": aps / 2}})
        else:
            aps = float(form.min_attacks_per_second.data)
            query_and.append(
                {"properties.Attacks per Second": {"$gte": aps}})
    else:
        if form.max_attacks_per_second.data:
            aps = float(form.max_critical_strike_chance.data)
            query_and.append(
                {"properties.Attacks per Second": {"$lte": aps}})

    if form.min_armour.data:
        if form.max_armour.data:
            query_and.append(
                {"properties.Armour": {"$gte": form.min_armour.data,
                                       "$lte": form.max_armour.data}})
        else:
            query_and.append(
                {"properties.Armour": {"$gte": form.min_armour.data}})
    else:
        if form.max_armour.data:
            query_and.append(
                {"properties.Armour": {"$lte": form.max_armour.data}})

    if form.min_evasion.data:
        if form.max_evasion.data:
            query_and.append(
                {"properties.Evasion Rating": {"$gte": form.min_evasion.data,
                                               "$lte": form.max_evasion.data}})
        else:
            query_and.append(
                {"properties.Evasion Rating": {"$gte": form.min_evasion.data}})
    else:
        if form.max_evasion.data:
            query_and.append(
                {"properties.Evasion Rating": {"$lte": form.max_evasion.data}})

    if form.min_shield.data:
        if form.max_shield.data:
            query_and.append(
                {"properties.Energy Shield": {"$gte": form.min_shield.data,
                                              "$lte": form.max_shield.data}})
        else:
            query_and.append(
                {"properties.Energy Shield": {"$gte": form.min_shield.data}})
    else:
        if form.max_shield.data:
            query_and.append(
                {"properties.Energy Shield": {"$lte": form.max_shield.data}})


    if form.min_quality.data:
        if form.max_quality.data:
            query_and.append(
                {"properties.Quality": {"$gte": form.min_quality.data,
                                              "$lte": form.max_quality.data}})
        else:
            query_and.append(
                {"properties.Quality": {"$gte": form.min_quality.data}})
    else:
        if form.max_quality.data:
            query_and.append(
                {"properties.Quality": {"$lte": form.max_quality.data}})



    if form.mods_name.data:
        if form.mods_lower_bound.data:
            if form.mods_upper_bound.data:
                query_and.append(
                    {"Mods."+form.mods_name.data: {"$gte": form.mods_lower_bound.data,
                                            "$lte": form.mods_upper_bound.data}})
            else:
                query_and.append(
                    {"Mods."+form.mods_name.data: {"$gte": form.mods_lower_bound.data}})

        elif form.mods_upper_bound.data:
            query_and.append(
                {"Mods." + form.mods_name.data: {"$lte": form.mods_upper_bound.data}})
        else:
            query_and.append(
                {"Mods." + form.mods_name.data: {"$exists": True}})


    return query_and
