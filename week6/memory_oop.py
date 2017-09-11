# implementation of card game - Memory

import simpleguitk as simplegui
import random


class Memory:
    def __init__(self):
        self.turns = 0
        self.card_list = [[1, 0], [1, 0], [2, 0], [2, 0], [3, 0],
                          [3, 0], [4, 0], [4, 0], [5, 0], [5, 0], [6, 0],
                          [6, 0], [7, 0], [7, 0], [8, 0], [8, 0]]

        self.clicked_cards_list = []


    # helper function to initialize globals
    def new_game(self):

        self.clicked_cards_list = []
        self.turns = 0
        for card in self.card_list:
            card[1] = 0
        random.shuffle(self.card_list)


    # define event handlers
    def mouseclick(self, pos):

        clicked_card = pos[0] / 50 % 16
        if self.card_list[clicked_card][1] == 0:
            self.card_list[clicked_card][1] = 1
            self.clicked_cards_list.append([self.card_list[clicked_card], clicked_card])

        if len(self.clicked_cards_list) == 2:
            if self.clicked_cards_list[0][0][0] == self.clicked_cards_list[1][0][0]:
                self.card_list[self.clicked_cards_list[0][1]][1] = 2
                self.card_list[self.clicked_cards_list[1][1]][1] = 2
                self.clicked_cards_list = []
                self.turns += 1
        elif len(self.clicked_cards_list) == 3:
            self.card_list[self.clicked_cards_list[0][1]][1] = 0
            self.card_list[self.clicked_cards_list[1][1]][1] = 0
            self.clicked_cards_list.pop(0)
            self.clicked_cards_list.pop(0)
            self.turns += 1


        # cards are logically 50x100 pixels in size

    def draw(self, canvas):
        idx = 1
        for card in self.card_list:
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
        label.set_text("Turns = " + str(self.turns))


mem = Memory()
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", mem.new_game())
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mem.mouseclick)
frame.set_draw_handler(mem.draw)

# get things rolling
frame.start()