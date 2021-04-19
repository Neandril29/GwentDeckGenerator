from db_helper import *
import itertools
import random
from colorama import Fore

version = "8.4.0"


# Récupération du leader
def get_leader():
    connection = create_connection("gwentdb", "postgres", "admin", "localhost", "5432")

    req_leader_data = "SELECT * FROM card.data WHERE attributes ->> 'type' like '%Ability%'" \
                      "AND version LIKE '" + version + "' ORDER BY " \
                                                       "RANDOM() LIMIT 1"
    res_leader = exec_read_query(connection, req_leader_data)
    req_leader_locale = "SELECT * FROM card.locale_fr WHERE i = " + str(res_leader[0][0])

    leader_name = exec_read_query(connection, req_leader_locale)[0][1]
    leader_faction = res_leader[0][3]['faction']
    leader_provisions = res_leader[0][3]['provision']
    leader_total_provision = 150 + leader_provisions

    leader_result = [leader_name, leader_faction, leader_total_provision]

    return leader_result


# Récupération du stratagème
def get_stratagem(faction):
    connection = create_connection("gwentdb", "postgres", "admin", "localhost", "5432")

    req_stratagem_data = "SELECT * FROM card.data WHERE ((attributes ->> 'type' like '%Stratagem%') " + \
                         "AND (attributes ->> 'faction' = '" + faction + "'" + \
                         "OR attributes ->> 'faction' = 'Neutral')) AND version " \
                         "LIKE '" + version + "' ORDER BY RANDOM() LIMIT 1 "

    res_stratagem = exec_read_query(connection, req_stratagem_data)
    req_stratagem_locale = "SELECT * FROM card.locale_fr WHERE i = " + str(res_stratagem[0][0])

    stratagem_name = exec_read_query(connection, req_stratagem_locale)[0][1]
    stratagem_faction = res_stratagem[0][3]['faction']

    stratagem_result = [stratagem_name, stratagem_faction]

    return stratagem_result


# Génération d'une carte
def get_card(faction, is_devotion):
    connection = create_connection("gwentdb", "postgres", "admin", "localhost", "5432")

    if is_devotion:
        req_card_data = "SELECT * FROM card.data WHERE (attributes ->> 'faction' = '" + faction + "') " + \
                        "AND (attributes ->> 'provision' NOT LIKE '0') " + \
                        "AND (attributes ->> 'type' NOT LIKE '%Ability%') " \
                        "AND (attributes ->> 'set' NOT LIKE 'NonOwnable') " + \
                        "AND (version LIKE '" + version + "') ORDER BY RANDOM() LIMIT 1"
    else:
        req_card_data = "SELECT * FROM card.data WHERE (attributes ->> 'faction' = '" + faction + "'" + \
                        "OR attributes ->> 'faction' = 'Neutral') " + \
                        "AND (attributes ->> 'provision' NOT LIKE '0') " + \
                        "AND (attributes ->> 'type' NOT LIKE '%Ability%')" + \
                        "AND (attributes ->> 'type' NOT LIKE '%Stratagem%')" + \
                        "AND (attributes ->> 'set' NOT LIKE 'NonOwnable') " + \
                        "AND (version LIKE '" + version + "') ORDER BY RANDOM() LIMIT 1"

    # "' OR attributes ->> 'faction' = 'Neutral')" \

    res_card = exec_read_query(connection, req_card_data)

    card_id = res_card[0][0]
    card_faction = res_card[0][3]['faction']
    card_provisions = res_card[0][3]['provision']
    card_rarity = res_card[0][3]['rarity']

    req_card_locale = "SELECT * FROM card.locale_fr WHERE i = " + str(card_id)
    card_name = exec_read_query(connection, req_card_locale)[0][1]

    card_result = [card_name, card_faction, card_provisions, card_rarity]

    return card_result


# Génération du deck complet
def deck_generator(iter_nb, faction, leader, stratagem, card_list, max_prov, is_devotion):
    print(f"{Fore.RED}EN COURS ... VEUILLEZ PATIENTER ...")
    print(f"{Fore.RED}VOTRE DECK VA APPARAÎTRE DANS QUELQUES INSTANTS\n")
    should_restart = True

    while should_restart:
        for i in range(iter_nb):
            card_to_append = get_card(faction, is_devotion)
            if card_to_append[3] == "Epic" or card_to_append[3] == "Legendary":
                if card_to_append in card_list:
                    card_list.remove(card_to_append)
                else:
                    card_list.append(card_to_append)
            elif card_to_append[3] == 'Rare' or card_to_append[3] == 'Common':
                if card_list.count(card_to_append) >= 2:
                    card_list.remove(card_to_append)
                else:
                    card_list.append(card_to_append)

            temp = []
            for j in range(len(card_list)):
                temp.append(card_list[j][2])

            if sum(temp) > max_prov:
                for _ in itertools.repeat(None, 5):
                    to_remove = random.choice(card_list)
                    card_list.remove(to_remove)
                should_restart = True
            elif (sum(temp) == max_prov) or (
                    (sum(temp) + 1 == max_prov) or
                    (sum(temp) + 2 == max_prov) or
                    (sum(temp) + 3 == max_prov)
            ):
                if len(card_list) < 25:
                    should_restart = True
                elif len(card_list) >= 25:
                    should_restart = False
                    break
                else:
                    should_restart = True

    whole_deck = [card_list, faction, leader, stratagem, str(len(card_list)), max_prov]

    return whole_deck
