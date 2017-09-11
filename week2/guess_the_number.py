# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simpleguitk as simplegui
import random
import math

secret_number = 0
guess = 0
range = 100
max_guesses = 0
guesses_left = 0

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global guess, range, secret_number, max_guesses, guesses_left

    print("----------------")
    print("----------------")
    print("New game started")
    print("----------------")
    secret_number = random.randrange(0, range + 1)
    max_guesses = math.ceil(math.log(range + 1) / math.log(2))
    guesses_left = max_guesses
    print ("You have", guesses_left, "guesses left")


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global range
    range = 100

    new_game()


def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global range
    range = 1000

    new_game()


def input_guess(guess):
    # main game logic goes here
    global guesses_left

    guess = int(guess)
    print("The player guess was", guess)
    print(secret_number)

    if guess == secret_number:
        print("Good job.", guess, "is the correct number!")

        new_game()
        return
    elif guess < secret_number:
        result = "lower"
    else:
        result = "higher"

    guesses_left = guesses_left - 1
    if guesses_left == 0:
        print("No more guesses. You lose!")
        print("Game over")

        new_game()
        return
    else:
        print("The guess was", result, "than the secret number. You have", guesses_left, "guesses left")
        print()

# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
f.add_button("Range is [0, 100]", range100, 200)
f.add_button("Range is [0, 1000]", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

new_game()

f.start()

