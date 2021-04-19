from generator import *
from colorama import Fore
from operator import itemgetter

# Variables
leader = get_leader()
leader_name = leader[0]
leader_faction = leader[1]
leader_provs = leader[2]

stratagem = get_stratagem(leader_faction)

stratagem_name = stratagem[0]
stratagem_faction = stratagem[1]

deck_min_cards = 25
cardList = []

# Saisie utilisateur
while True:
    user_input = input("Quel type de deck souhaitez vous générer : \n [1] : Dévotion \n [2] : Standard \n")
    if user_input in ['1', '2']:
        break

if user_input == '1':
    the_deck = deck_generator(deck_min_cards,
                              leader_faction,
                              leader_name,
                              stratagem_name,
                              cardList,
                              leader_provs,
                              True)
elif user_input == '2':
    the_deck = deck_generator(deck_min_cards,
                              leader_faction,
                              leader_name,
                              stratagem_name,
                              cardList,
                              leader_provs,
                              False)
else:
    the_deck = None
    print("Mauvais choix")


# Résultat final du deck
def print_whole_deck(deck):
    deck_list = deck[0]
    deck_faction = str(deck[1])
    deck_leader = str(deck[2])
    deck_stratagem = str(deck[3])
    deck_length = str(deck[4])
    deck_provs = str(deck[5])

    print(f"{Fore.CYAN}Votre deck est prêt (il contient " + deck_length + " cartes) !")
    print(f"{Fore.CYAN}Votre faction : " + deck_faction + " , avec le leader " + deck_leader + \
          " (" + deck_provs + " provisions), et votre stratagème " + deck_stratagem)

    deck_list = sorted(deck_list, key=itemgetter(2), reverse=True)

    for i in range(len(deck_list)):
        print(f"{Fore.YELLOW}Carte : " + str(deck_list[i][0]), f"{Fore.MAGENTA}, Faction : " + \
              str(deck_list[i][1]) + f"{Fore.GREEN}, Provisions : " + str(deck_list[i][2]))


print_whole_deck(the_deck)
