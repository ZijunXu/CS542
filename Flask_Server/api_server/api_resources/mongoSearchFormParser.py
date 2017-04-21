def parser(form):
    query_and = []

    if form.currency_name.data:
        if form.min_price.data:
            if form.max_price.data:
                query_and.append({"Price.Currency": form.currency_name.data,
                                  "Price.Number": {"$gte": form.min_price.data, "$lt": form.max_price.data}})
            else:
                query_and.append({"Price.Currency": form.currency_name.data,
                                  "Price.Number": {"$gte": form.min_price.data}})
        else:
            query_and.append({"Price.Currency": form.currency_name.data})

    if form.name.data:
        query_and.append({"name": form.name.data})

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
            query_and.append({"ilvl": {"$gte": form.min_ilvl.data, "$lt": form.max_ilvl.data}})
        else:
            query_and.append({"ilvl": {"$gte": form.min_ilvl.data}})

    if form.min_socket_number.data:
        if form.max_socket_number.data:
            query_and.append({"sockets.socket_number": {"$gte": form.min_socket_number.data,
                                                        "$lt": form.max_socket_number.data}})
        else:
            query_and.append({"sockets.socket_number": {"$gte": form.min_socket_number.data}})

    if form.min_link_number.data:
        if form.max_link_number.data:
            query_and.append({"sockets.link": form.max_link_number.data})
        else:
            query_and.append({"sockets.link": form.min_link_number.data})

    if form.min_str_socket:
        query_and.append({"sockets.S": {"$gte": form.min_str_socket.data}})

    if form.min_dex_socket:
        query_and.append({"sockets.D": {"$gte": form.min_dex_socket.data}})

    if form.min_int_socket:
        query_and.append({"sockets.I": {"$gte": form.min_int_socket.data}})

    if form.min_other_socket:
        query_and.append({"sockets.Other": {"$gte": form.min_other_socket.data}})

    # requirements
    if form.min_requirements_int.data:
        if form.max_requirements_int.data:
            query_and.append(
                {"requirements.Int": {"$gte": form.min_requirements_int.data,
                                      "$lt": form.max_requirements_int.data}})
        else:
            query_and.append(
                {"requirements.Int": {"$gte": form.min_requirements_int.data}})
    elif form.min_requirements_dex.data:
        if form.max_requirements_dex.data:
            query_and.append(
                {"requirements.Dex": {"$gte": form.min_requirements_dex.data,
                                      "$lt": form.max_requirements_dex.data}})
        else:
            query_and.append(
                {"requirements.Dex": {"$gte": form.min_requirements_dex.data}})
    elif form.min_requirements_str.data:
        if form.max_requirements_str.data:
            query_and.append(
                {"requirements.Str": {"$gte": form.min_requirements_str.data,
                                      "$lt": form.max_requirements_str.data}})
        else:
            query_and.append(
                {"requirements.Str": {"$gte": form.min_requirements_str.data}})
    elif form.min_requirements_lvl.data:
        if form.max_requirements_lvl.data:
            query_and.append(
                {"requirements.Level": {"$gte": form.min_requirements_lvl.data,
                                        "$lt": form.max_requirements_lvl.data}})
        else:
            query_and.append(
                {"requirements.Level": {"$gte": form.min_requirements_lvl.data}})

    # properties
    if form.physical_damage.data:
        query_and.append(
            {"properties.Physical Damage": {"$gte": form.physical_damage.data}})

    if form.elemental_damage.data:
        query_and.append(
            {"properties.Elemental Damage": {"$gte": form.elemental_damage.data}})

    if form.min_critical_strike_chance.data:
        if form.max_critical_strike_chance.data:
            query_and.append(
                {"properties.Critical Strike Chance": {"$gte": form.min_critical_strike_chance.data,
                                                       "$lt": form.max_critical_strike_chance.data}})
        else:
            query_and.append(
                {"properties.Critical Strike Chance": {"$gte": form.min_critical_strike_chance.data}})

    if form.min_attacks_per_second.data:
        if form.max_attacks_per_second.data:
            query_and.append(
                {"properties.Attacks per Second": {"$gte": form.min_attacks_per_second.data,
                                                   "$lt": form.max_attacks_per_second.data}})
        else:
            query_and.append(
                {"properties.Attacks per Second.data": {"$gte": form.min_attacks_per_second.data}})

    if form.min_armour.data:
        if form.max_armour.data:
            query_and.append(
                {"properties.Armour": {"$gte": form.min_armour.data,
                                       "$lt": form.max_armour.data}})
        else:
            query_and.append(
                {"properties.Armour": {"$gte": form.min_armour.data}})

    if form.min_evasion.data:
        if form.max_evasion.data:
            query_and.append(
                {"properties.Evasion Rating": {"$gte": form.min_evasion.data,
                                               "$lt": form.max_evasion.data}})
        else:
            query_and.append(
                {"properties.Evasion Rating": {"$gte": form.min_evasion.data}})

    if form.min_shield.data:
        if form.max_shield.data:
            query_and.append(
                {"properties.Energy Shield": {"$gte": form.min_shield.data,
                                              "$lt": form.max_shield.data}})
        else:
            query_and.append(
                {"properties.Energy Shield": {"$gte": form.min_shield.data}})

    return query_and
