# Mini-project #6 - Blackjack

import random

import simpleguitk as simplegui


# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
# bei dropbox /dl=1 anhaengen
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')  # Club, Spade, Heart, Diamond
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def get_value(self):
        return VALUES[self.rank]

    def draw(self, canvas, pos, back=False):
        if back == False:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                              CARD_SIZE)
        else:
            canvas.draw_image(card_back, [CARD_CENTER[0], CARD_CENTER[1]], CARD_SIZE,
                              [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                              CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ret = ""
        for c in self.cards:
            ret += str(c) + " "

        return ret

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        aces = False
        for card in self.cards:
            value += card.get_value()
            if card.rank == 'A':
                aces = True

        if aces == False:
            return value
        else:
            if value + 10 <= 21:
                return value + 10
            else:
                return value


    def draw(self, canvas, pos, first_back=False):
        """ pos is the start left side position for the hand """
        start_pos = pos[0]
        for card in self.cards:
            pos[0] = start_pos + self.cards.index(card) * CARD_SIZE[0]
            if first_back == True and self.cards.index(card) == 0:
                card.draw(canvas, pos, True)
            else:
                card.draw(canvas, pos)



# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))
        self.shuffle()

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(0)

    def __str__(self):
        ret = ""
        for d in self.deck:
            ret += str(d) + " "

        return ret


class Blackjack:
    score = 0


    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.outcome = "Hit or stand"

    # define event handlers for buttons
    def deal(self):

        self.__init__()

        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.check_for_winloose()

        self.in_play = True

    def check_for_winloose(self):
        if self.player_hand.get_value() == 21:
            self.outcome = "Player wins"
            self.score += 1
            self.in_play = False
        elif self.player_hand.get_value() > 21:
            self.outcome = "Player busted"
            self.score -= 1
            self.in_play = False

    def hit(self):
        """
            if the hand is in play, hit the player
            if busted, assign a message to outcome, update in_play and score
        """
        if self.in_play == True:
            self.player_hand.add_card(self.deck.deal_card())
            self.check_for_winloose()


    def stand(self):
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        # assign a message to outcome, update in_play and score

        if self.in_play == True:
            while True:
                dealer_value = self.dealer_hand.get_value()
                if dealer_value >= 17 and dealer_value <= 21:
                    if dealer_value < self.player_hand.get_value():
                        self.outcome = "Player wins"
                        self.score += 1
                    else:
                        self.outcome = "Dealer wins"
                        self.score -= 1
                    break
                elif dealer_value > 21:
                    self.outcome = "Player wins"
                    self.score += 1
                    break

                self.dealer_hand.add_card(self.deck.deal_card())

        self.in_play = False

    # draw handler
    def draw(self, canvas):
        # def draw_text(self, text, point, font_size, font_color, font_face='serif'):
        canvas.draw_text("Blackjack", [50, 50], 30, "Black")
        canvas.draw_text("Score: ", [250, 50], 16, "Black")
        canvas.draw_text(str(self.score), [350, 50], 16, "Black")

        canvas.draw_text("Dealer", [50, 150], 25, "Black")
        # canvas.draw_text(str(self.dealer_hand.get_value()), [50, 200], 10, "Black")
        self.dealer_hand.draw(canvas, [100, 200], self.in_play)

        canvas.draw_text("Player", [50, 350], 25, "Black")
        canvas.draw_text(self.outcome, [400, 350], 20, "Black")
        #        canvas.draw_text(str(self.player_hand.get_value()), [50, 400], 10, "Black")
        self.player_hand.draw(canvas, [100, 400])


    def run(self):
        # initialization frame
        self.frame = simplegui.create_frame("Blackjack", 600, 600)
        self.frame.set_canvas_background("Green")

        # create buttons and canvas callback
        self.frame.add_button("Deal", self.deal, 200)
        self.frame.add_button("Hit", self.hit, 200)
        self.frame.add_button("Stand", self.stand, 200)
        self.frame.set_draw_handler(self.draw)

        # get things rolling
        self.deal()
        self.frame.start()


if __name__ == '__main__':
    bj = Blackjack()
    bj.run()