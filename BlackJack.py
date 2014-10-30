'''
####################################
# Robert Hood                      #
# An Introduction to Interactive   #
#  Programming in Python           #
#                                  #
# Programmign Project              #
#    Blackjack                     #
#                                  #
####################################
____________________________________
Mini-project description - Blackjack
Blackjack is a simple, popular card game that is played in many casinos. Cards in Blackjack have the following 
values: an ace may be valued as either 1 or 11 (player's choice), face cards (kings, queens and jacks) are valued 
at 10 and the value of the remaining cards corresponds to their number. During a round of Blackjack, the players 
plays against a dealer with the goal of building a hand (a collection of cards) whose cards have a total value 
that is higher than the value of the dealer's hand, but not over 21.  (A round of Blackjack is also sometimes 
referred to as a hand.)
The game logic for our simplified version of Blackjack is as follows. The player and the dealer are each dealt 
two cards initially with one of the dealer's cards being dealt faced down (his hole card). The player may then 
ask for the dealer to repeatedly "hit" his hand by dealing him another card. If, at any point, the value of the 
player's hand exceeds 21, the player is "busted" and loses immediately. At any point prior to busting, the player 
may "stand" and the dealer will then hit his hand until the value of his hand is 17 or more. (For the dealer, 
aces count as 11 unless it causes the dealer's hand to bust). If the dealer busts, the player wins. Otherwise, 
the player and dealer then compare the values of their hands and the hand with the higher value wins. The dealer 
wins ties in our version.
____________________________________

Please note I am siteing the following sources for inspiration for my original Code
This Course and it's great professors:
http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00sc-introduction-to-computer-science-and-programming-spring-2011/index.htm
http://learnpythonthehardway.org/book/
http://www.diveintopython.net/toc/index.html
http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html
https://en.wikibooks.org/wiki/Python_Programming
____________________________________

For Ease of Creation I'm Useing the 7 Parts of Programming Structure (Modified to 8)
0. Import Python Modules and External Graphics
1. Globals (states)
2. Helper Functions (N/A)
3. Classes
4. Define Event Handlers
5. Create a Frame (create frame, buttons, canvas)
6. Register Event Handlers
7. start frame and timers

Code Start
____________________________________
'''

# 0. Import Python Modules and External Graphics
import simplegui
import random
    # load card sprites - 949x392 - source: jfitz.com reloacted to my Dropbox (Note dl=1 needed to allow download and use)
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("https://www.dropbox.com/s/dbj2k5vvio2dwnx/cards.jfitz.png?dl=1")
CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("https://www.dropbox.com/s/16jc98xc1azdeud/card_back.png?dl=1")


# 1. Globals (states)
in_play = False
outcome = "Hit or Stand?"
PlayerScore = 0
DealerScore = 0
                                            # define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# 3. Classes
class Card:                                 # define card class
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
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

class Hand:                                 # define hand class
    def __init__(self):                     # create Hand object
        self.cards = []
    def __str__(self):                      # return a string representation of a hand
        result = ""
        for card in self.cards:
            result += " " + card.__str__()
        return "Hand contains" + result
    def add_card(self, card):               # add a card object to a hand
        self.cards.append(card)
    def get_value(self):                    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        contains_ace = False
        for card in self.cards:
            rank = card.get_rank()
            value += VALUES[rank]
            if(rank == 'A'):
                contains_ace = True
        if(value < 11 and contains_ace):    # compute the value of the hand, see Blackjack video
            value += 10
        return value
    def draw(self, canvas, pos):            # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 80

class Deck:                                 # define deck class
    def __init__(self):                     # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
    def shuffle(self):                      # shuffle the deck 
        random.shuffle(self.cards)          # use random.shuffle()
    def deal_card(self):                    # deal a card object from the deck
        return self.cards.pop(0)
    def __str__(self):                      # return a string representing the deck
        result = ""
        for card in self.cards:
            result += " " + card.__str__()
        return "Deck Contains" + result


# 4. Define Event Handlers
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, deck, DealerScore
    if(in_play == True):
        outcome = "You lost because of re-deal! Deal Again?"
        DealerScore += 1
        in_play = False
    else:
        deck = Deck()
        outcome
        deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        print "Player: %s" % player_hand
        print "Dealer: %s" % dealer_hand
        in_play = True

def hit():
    global outcome, in_play, DealerScore
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
        print "Player hand %s" % player_hand
        if player_hand.get_value() > 21:
            outcome = "You Busted! New Deal?"
            in_play = False
            print outcome
            DealerScore += 1

def stand():
    global outcome, PlayerScore, DealerScore, in_play
    in_play = False
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
    print "Dealer: %s" % dealer_hand
    if dealer_hand.get_value() > 21:
        outcome = "Dealer busted. Congratulations!"
        print outcome
        PlayerScore += 1
    else:
        if dealer_hand.get_value() >= player_hand.get_value() or player_hand.get_value() > 21:
            outcome = "Dealer wins. New deal?"
            print outcome
            DealerScore += 1
        else:
            outcome = "Player wins, New Deal?"
            print outcome
            PlayerScore += 1

def draw(canvas):
    global outcome, in_play, card_back, card_loc, PlayerScore, DealerScore
    canvas.draw_text("Blackjack", [220, 50], 48 ,"White")
    player_hand.draw(canvas, [100, 300])
    dealer_hand.draw(canvas, [100, 150])
    canvas.draw_text(outcome, [10, 100], 36 ,"White")
    canvas.draw_text("Dealer: %s" % DealerScore, [10, 150], 20 ,"Black")
    canvas.draw_text("Player: %s" % PlayerScore, [10, 300], 20 ,"Black")
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (136,199), CARD_BACK_SIZE)


# 5. Create a Frame (create frame, buttons, canvas)
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# 6. register Event Handlers
deal()


# 7. start frame and timers
frame.start()