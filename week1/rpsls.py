# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions
import random

def name_to_number(name):
    # convert name to number using if/elif/else
    # don't forget to return the result!
    if name == 'rock':
        ret = 0
    elif name == 'Spock':
        ret = 1
    elif name == 'paper':
        ret = 2
    elif name == 'lizard':
        ret = 3
    elif name == 'scissors':
        ret = 4
    else:
        print("Error")
        ret = 0

    return ret

def number_to_name(number):
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    if number == 0:
        ret = 'rock'
    elif number == 1:
        ret = 'Spock'
    elif number == 2:
        ret = 'paper'
    elif number == 3:
        ret = 'lizard'
    elif number == 4:
        ret = 'scissors'
    else:
        print("Error")
        ret = 0

    return ret

def rpsls(player_choice):
    # print a blank line to separate consecutive games
    print()
    # print out the message for the player's choice
    print("Player chooses ", player_choice)
    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    # print out the message for computer's choice
    print("Computer chooses ", comp_choice)
    # compute difference of comp_number and player_number modulo five
    diff = (comp_number - player_number ) % 5
    # use if/elif/else to determine winner, print winner message
    if diff == 1 or diff == 2:
        print("Computer wins!")
    elif diff == 3 or diff == 4:
        print("Player wins!")
    else:
        print("Player and computer tie!")

# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
rpsls("s")

# always remember to check your completed program against the grading rubric
