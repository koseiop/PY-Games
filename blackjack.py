import sys
import os
sys.path.append(os.path.abspath("D:/Documents/Python/game"))

import random
from time import sleep

from player import Player

###########################
# Changes #
###########

# Added option for Players to split their hands
# if the first two cards dealt are of same value
# inc 10 value cards.
##
# Added hands matrix to Player to represent multiple player hands and scores
# Modified functions and code to deal with this change
#
###########
###########################

def values(card):
    value = 0
    if (card[0] == "J") or (card[0] == "Q") or (card[0] == "K"):
        value = 10
    elif card[0] == "A":
        value = 11#[1, 11]
    elif len(card) == 2:
        value = int(card[0])
    else:
        value = int(card[0:2])
    return value


def deal(deck, player):
    dealt_card = deck.pop()
    sleep(1)
    print(f"{player} your card is {dealt_card}")
    sleep(1)
    player.hands[0].append(dealt_card)
    player.hands[0][0] += values(dealt_card)
    if len(player.hands[0]) == 3:
        player.fake.append(dealt_card)
        print(f"{player} has {player.fake} score is {values(dealt_card)}\n")
    else:
        print(f"{player} has {player.hands[0][1:]} score is {player.hands[0][0]}")

def deal_split(deck, player, hand):
    dealt_card = deck.pop()
    sleep(1)
    print(f"{player} your card is {dealt_card}")
    sleep(1)
    hand.append(dealt_card)
    hand[0] += values(dealt_card)
    print(f"{player} has {hand[1:]} score is {hand[0]}")

def deal_fd(deck, player):
    dealt_card = deck.pop()
    sleep(1)
    print(f"{player} has been dealt a card face down\n")
    sleep(1)
    player.hands[0].append(dealt_card)
    player.hands[0][0] += values(dealt_card)
    player.fake.append("X")

def winners(stand_list, win_list, dealer):
    tie = []
    if stand_list:
        if dealer.hands[0][0] > 21:
            print(f"{dealer.name} hand is bust")
            for i in stand_list:
                win_list.append(i)
        for i in stand_list:
            if (i.hands[0][0] > dealer.hands[0][0]) and (i.hands[0][0] > 21) \
            or (i.hands[1][0] > dealer.hands[0][0]) and (i.hands[1][0] > 21): # one of players hands in stand list other is bust
                # no bueno
                pass
            if (i.hands[0][0] > dealer.hands[0][0]) and (i.hands[0][0] < 21): # first hand beats dealer
                win_list.append(i)
            if (i.hands[1][0] > dealer.hands[0][0]) and (i.hands[1][0] < 21): # second hand beats dealer
                win_list.append(i)
            if (i.hands[0][0] == dealer.hands[0][0]) and (i.hands[0][0] < 21): # first hand draws
                tie.append(i)
            if (i.hands[1][0] == dealer.hands[0][0]) and (i.hands[1][0] < 21): # second hand draws
                tie.append(i)
    if win_list or tie:
        if win_list:
            if dealer.hands[0][0] == 21: # Players added to win_list if blackjack need to be treated as drawn if dealer has 21
                print(f"The following have drawn with {dealer} on {dealer.hands[0][0]}....")
                print(", ".join([i.name for i in win_list]))
            else:
                print("The winner(s) are.....")
                print(", ".join([i.name for i in win_list]))
        if tie:
            print(f"The following have drawn with {dealer} on {dealer.hands[0][0]}....")
            print(", ".join([i.name for i in tie]))
    else:
        print(f"{dealer.name} wins!")


def round(deck, dealer, players):
    # shufle cards
    for i in range(random.randint(1, 4)):
        random.shuffle(deck)
    # deal first card face down
    for player in players:
        deal_fd(deck, player)
    deal_fd(deck, dealer)
    # deal second card face up
    for player in players:
        deal(deck, player)
    deal(deck, dealer)


def player_choice(player, hand, win_list, stand_list):
    played = False
    while played == False:
        if player.hands[0][0] == 21:
            print(f"{player} has a blackjack! *{hand[1:]}*\n")
            win_list.append(player)
            break
        player.choice = input(f"{player} your cards are {hand[1:]} score is {hand[0]}, hit or stand? (input hit or stand): ")
        print(player.choice)
        if player.choice.lower() == "stand":
            print(f"{player} stands on {hand[0]}\n")# score
            stand_list.append(player)
            break
        elif player.choice.lower() == "hit":
            if (len(player.hands[0]) > 1) and (len(player.hands[1]) > 1): # split hands
                deal_split(deck, player, hand)
            else:
                deal(deck, player)
            if hand[0] == 21:
                print(f"{player} has a blackjack!\n")
                win_list.append(player)
                played = True

            elif hand[0] > 21:
                print(f"{player} is bust with {hand[0]}\n")
                played = True

        else:
            print(f"Did not recognise {player.choice} please enter hit or stand.")


game_state = True
while game_state == True:

    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    suits = ["H", "C", "S", "D"]

    deck = [i+p for p in suits for i in cards]

    dealer = Player("The Dealer")

    valid_game = False
    while not valid_game:
        try:
            player_number = int(input("How many players will play? (1-6): "))
            if (player_number > 0) and (player_number < 7):
                valid_game = True
                player_list = [i for i in range(player_number)]
            else:
                raise ValueError(f'You did not select a number between 1 or 6 ({player_number}).')
        except ValueError as e:
            print("Error.", e.args)

    players_list = ["player"+str(i + 1) for i in player_list]
    #print(players_list)
    print("Welcome "+ ", ".join([player for player in players_list])+".\n")
    players = []


    for player in players_list:
        player = Player(player)
        players.append(player)

    win_list = []
    stand_list = []
    insurance_list = []
    ######################### First Round #######################
    ######################### Second Round ######################
    round(deck, dealer, players)
    #############################################################
    ####################### INSURANCE ###########################
    #print(dealer.hands[0][1][0])
    if dealer.hands[0][2][0] == "A":
        for player in players:

            player.choice = input(f"{dealer} has an Ace, {player} would you like to purchace insurance? (y/n): ")
            print(player.choice)
            if (player.choice.lower == "y"): #or (player.choice.lower == "yes"):
                insurance_list.append(player)
                print(f"{player} has chosen insurance.\n")
                valid_choice = True
            elif (player.choice.lower == "n"):# or (player.choice.lower == "no"):
                print(f"{player} declines insurance.\n")
                valid_choice = True
            else:
                # print(f"Did not recognise the input {player} insurance declined.")
                print(f"Did not recognise the input {player} try again.")
    #############################################################

    for player in players:

            # if player.hands[0][1][0] == player.hands[0][2][0]:
            if values(player.hands[0][1]) == values(player.hands[0][2]):# will be able to split with all 10 value cards as well
                print(f"Split available {player}!")
                player.choice = input(f"{player} your cards are {player.hands[0][1:]} score is {player.hands[0][0]}, would you like to split your hand? (y/n): ")
                print(player.choice)
                if player.choice.lower() == "y":
                    move_card = player.hands[0].pop()
                    player.hands[0][0] //= 2
                    print(move_card)
                    player.hands[1].append(move_card)
                    player.hands[1][0] = player.hands[0][0]


                    for hand in player.hands:
                        print(hand)
                        player_choice(player, hand, win_list, stand_list)

                else:
                    print(f"{player} has declined the split\n")
                    player_choice(player, player.hands[0], win_list, stand_list)
            else:
                player_choice(player, player.hands[0], win_list, stand_list)


    print(f"{dealer} has {dealer.hands[0][1:]}")
    sleep(2)
    if dealer.hands[0][0] < 17:
        print(f"{dealer.name} has a score of {dealer.hands[0][0]} and will draw cards until they reach a score of 17 or more.....\n")
        while dealer.hands[0][0] < 17:
            deal(deck, dealer)
            print(dealer.hands[0][0])
    elif (dealer.hands[0][0] > 16) or (dealer.hands[0][0] < 21):
        print(f"{dealer.name} has a score of {dealer.hands[0][0]} and will stand")
    elif (dealer.hands[0][0] == 21) and win_list:
        print(f"{dealer} and the following players have a blackjack...")
        for i in win_list:
            print(i)

    # Check for winners
    winners(stand_list, win_list, dealer)

    restart = input("Would you like to restart the game? (y/n) ")
    if restart.lower() == "y":
        print("Restarting...")
        sleep(2)
    elif restart.lower() == "n":
        print("Thank you for playing.")
        game_state = False
    else:
        print("Did not recognise that answer, ending game.")
        game_state = False
