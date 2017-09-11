# implementation of card game - Memory

import simpleguitk as simplegui
import random

card_list = [[1, 0], [1, 0], [2, 0], [2, 0], [3, 0], [3, 0], [4, 0], [4, 0], [5, 0], [5, 0], [6, 0], [6, 0], [7, 0],
             [7, 0], [8, 0], [8, 0]]

clicked_cards_list = []
turns = 0

# helper function to initialize globals
def new_game():
    global turns

    clicked_cards_list = []
    turns = 0
    for card in card_list:
        card[1] = 0
    random.shuffle(card_list)


# define event handlers
def mouseclick(pos):
    global clicked_cards_list, turns

    clicked_card = pos[0] / 50 % 16
    if card_list[clicked_card][1] == 0:
        card_list[clicked_card][1] = 1
        clicked_cards_list.append([card_list[clicked_card], clicked_card])

    if len(clicked_cards_list) == 2:
        if clicked_cards_list[0][0][0] == clicked_cards_list[1][0][0]:
            card_list[clicked_cards_list[0][1]][1] = 2
            card_list[clicked_cards_list[1][1]][1] = 2
            clicked_cards_list = []
            turns += 1
    elif len(clicked_cards_list) == 3:
        card_list[clicked_cards_list[0][1]][1] = 0
        card_list[clicked_cards_list[1][1]][1] = 0
        clicked_cards_list.pop(0)
        clicked_cards_list.pop(0)
        turns += 1


# cards are logically 50x100 pixels in size
def draw(canvas):
    idx = 1
    for card in card_list:
        if card[1] > 0:
            canvas.draw_polygon(
                [[idx * 50 - 50, 0], [idx * 50, 0], [idx * 50, 100], [idx * 50 - 50, 100], [idx * 50 - 50, 0]],
                2, 'Yellow', 'Black')
            canvas.draw_text(str(card[0]), [(idx * 50) - 30, 70], 40, "White")
        else:
            canvas.draw_polygon(
                [[idx * 50 - 50, 0], [idx * 50, 0], [idx * 50, 100], [idx * 50 - 50, 100], [idx * 50 - 50, 0]], 2,
                'Yellow', 'Green')

        idx += 1
    label.set_text("Turns = " + str(turns))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()