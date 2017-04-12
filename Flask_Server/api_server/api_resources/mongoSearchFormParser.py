def parser(form):
    query_and = []
    # requirements
    if form.data.min_requirements_int:
        if form.data.max_requirements_int:
            query_and.append(
                {"requirements.name": "Int", "requirements.values": {"$gte": form.data.min_requirements_int,
                                                                     "$lt": form.data.max_requirements_int}})
        else:
            query_and.append(
                {"requirements.name": "Int", "requirements.values": {"$gte": form.data.min_requirements_int}})
    elif form.data.min_requirements_dex:
        if form.data.max_requirements_dex:
            query_and.append(
                {"requirements.name": "Dex", "requirements.values": {"$gte": form.data.min_requirements_dex,
                                                                     "$lt": form.data.max_requirements_dex}})
        else:
            query_and.append(
                {"requirements.name": "Dex", "requirements.values": {"$gte": form.data.min_requirements_dex}})
    elif form.data.min_requirements_str:
        if form.data.max_requirements_str:
            query_and.append(
                {"requirements.name": "Str", "requirements.values": {"$gte": form.data.min_requirements_str,
                                                                     "$lt": form.data.max_requirements_str}})
        else:
            query_and.append(
                {"requirements.name": "Str", "requirements.values": {"$gte": form.data.min_requirements_str}})
    elif form.data.min_requirements_lvl:
        if form.data.max_requirements_lvl:
            query_and.append(
                {"requirements.name": "Level", "requirements.values": {"$gte": form.data.min_requirements_lvl,
                                                                       "$lt": form.data.max_requirements_lvl}})
        else:
            query_and.append(
                {"requirements.name": "Level", "requirements.values": {"$gte": form.data.min_requirements_lvl}})

    # properties
    if form.data.physical_damage:
        query_and.append(
            {"properties.name": "Physical Damage",
             "properties.values": {"$gte": form.data.physical_damage}})

    if form.data.elemental_damage:
        query_and.append(
            {"properties.name": "Elemental Damage",
             "properties.values": {"$gte": form.data.elemental_damage}})

    if form.data.min_critical_strike_chance:
        if form.data.max_critical_strike_chance:
            query_and.append(
                {"properties.name": "Critical Strike Chance",
                 "properties.values": {"$gte": form.data.min_critical_strike_chance,
                                       "$lt": form.data.max_critical_strike_chance}})
        else:
            query_and.append(
                {"properties.name": "Critical Strike Chance",
                 "properties.values": {"$gte": form.data.min_critical_strike_chance}})

    if form.data.min_attacks_per_Second:
        if form.data.max_attacks_per_Second:
            query_and.append(
                {"properties.name": "Attacks per Second",
                 "properties.values": {"$gte": form.data.min_attacks_per_Second,
                                       "$lt": form.data.max_attacks_per_Second}})
        else:
            query_and.append(
                {"properties.name": "Attacks per Second",
                 "properties.values": {"$gte": form.data.min_attacks_per_Second}})

    if form.data.min_armour:
        if form.data.max_armour:
            query_and.append(
                {"properties.name": "Armour",
                 "properties.values": {"$gte": form.data.min_armour,
                                       "$lt": form.data.max_armour}})
        else:
            query_and.append(
                {"properties.name": "Armour", "properties.values": {"$gte": form.data.min_armour}})

    if form.data.min_evasion:
        if form.data.max_evasion:
            query_and.append(
                {"properties.name": "Evasion Rating",
                 "properties.values": {"$gte": form.data.min_evasion,
                                       "$lt": form.data.max_evasion}})
        else:
            query_and.append(
                {"properties.name": "Evasion Rating", "properties.values": {"$gte": form.data.min_evasion}})

    if form.data.min_shiled:
        if form.data.max_shiled:
            query_and.append(
                {"properties.name": "Energy Shield",
                 "properties.values": {"$gte": form.data.min_shiled,
                                       "$lt": form.data.max_shiled}})
        else:
            query_and.append(
                {"properties.name": "Energy Shield", "properties.values": {"$gte": form.data.min_shiled}})

    return query_and
