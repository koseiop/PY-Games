import random

from player import Player

def choice(player1, player2):
    player_list = [player1, player2]
    choice_list = ["rock", "paper", "scissors"]

    if player2.name == "the computer": # Playing aginst the computer
        valid_choice = False
        while valid_choice == False:
            player1.choice = input(f"{player1} choose either rock, paper or scissors: ").lower()
            if player1.choice in choice_list:
                valid_choice = True
            else:
                print(f"{player1.choice} is not a valid choice {player1} please choose again.")
        player2.choice = choice_list[random.randint(0, 2)]
    else:
        for player in player_list:
            valid_choice = False
            while valid_choice == False:
                player.choice = input(f"{player} choose either rock, paper or scissors: ").lower()
                if player.choice in choice_list:
                    valid_choice = True
                else:
                    print(f"{player.choice} is not a valid choice {player} please choose again.")


def result(player1, player2):
    # Assign names to each player
    choice(player1, player2)


    if player1.choice == player2.choice: # Both players pick same choice
        print(f"You both picked {player1.choice}, this round is a draw")
    elif (player1.choice == "rock" and player2.choice == "scissors") \
    or (player1.choice == "scissors" and player2.choice == "paper") \
    or (player1.choice == "paper" and player2.choice == "rock"):
        # Each win condition for player one's choices
        print(f"{player1} choose {player1.choice} and {player2} choose {player2.choice}...")
        print(f"{player1} wins this round!")
        player1.score += 1 # Increase score of player1 by 1
    else: # If player one does not win plaer two must have won
        print(f"{player1} chose {player1.choice} and {player2} choose {player2.choice}...")
        print(f"{player2} wins this round!")
        player2.score += 1 # Increase score of player2 by 1

def scores(player1, player2):
    # Shows each players score
    print(f"{player1} has a score of {player1.score} and {player2} has a score of {player2.score}\n")


def win(player1, player2):
    if player1.score == 3:
        print(f"{player1} has won! Well done.")
        return True
    elif (player2.score == 3) and (player2.name == "the computer"):
        print(f"Bad luck {player1}, {player2.name} has won.")
        return True
    elif player2.score == 3:
        print(f"{player2} has won! Well done.")
        return True
    return False


game_state = True
while game_state == True:

    player_one = Player("Player One")
    player_two = Player("Player Two")

    valid_game = False
    #while valid_game == False:
    while not valid_game:
        try:
            game_type = int(input("Would you like to play against the computer(1) or another player(2) (1/2): "))
            # assert (game_type == 1) or (game_type == 2)
            if (game_type == 1) or (game_type == 2):
                valid_game = True
            else:
                raise ValueError(f'You did not enter either 1 or 2, ({game_type}).')

        except ValueError as e:
            print("Error: ", e.args)


    if game_type == 2:
        player_one.set_name()
        player_two.set_name()

        while not win(player_one, player_two):
            result(player_one, player_two)
            scores(player_one, player_two)

    elif game_type == 1:
        player_one.set_name()
        player_two.name = "the computer"

        while not win(player_one, player_two):
            result(player_one, player_two)
            scores(player_one, player_two)

    restart = input("Would you like to restart the game? (y/n) ")
    if restart.lower() == "y":
        print("Restarting...")
    elif restart.lower() == "n":
        print("Thank you for playing.")
        game_state = False
    else:
        print("Did not recognise that answer, ending game.")
        game_state = False
