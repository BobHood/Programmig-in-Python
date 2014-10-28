'''
####################################
# Robert Hood                      #
# An Introduction to Interactive   #
#  Programming in Python           #
#                                  #
# Programmign Project              #
#    Memory Game                   #
#                                  #
####################################

Please note I am siteing the following sources for inspiration for my original Code
This Course and it's great professors:
http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00sc-introduction-to-computer-science-and-programming-spring-2011/index.htm
http://learnpythonthehardway.org/book/
http://www.diveintopython.net/toc/index.html
http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html
https://en.wikibooks.org/wiki/Python_Programming

For Ease of Creation I'm Useing the 7 Parts of Programming Structure (Modified to 8)

0. Import Python Modules
1. Globals (states)
2. Helper Functions
3. Classes (N/A)
4. Define Event Handlers
5. Create a Frame
6. register Event Handlers (N/A)
7. start frame and timers

Memory is a card game in which the player deals out a set of cards face down.
In Memory, a turn (or a move) consists of the player flipping over two cards. If they match, 
the player leaves them face up. If they don't match, the player flips the cards back face down. 
The goal of Memory is to end up with all of the cards flipped face up in the minimum number of turns. 
A Memory Deck consists of eight pairs of matching cards.

Code Start
'''


# 0. Import Python Modules
import simplegui
import random

# 2. Helper Functions (Section 1. Globals moved here)
def Initialize():
    global Deck, CardExposed, State, CardIndexOne, CardIndexTwo, Score, NumOfMoves
    State, Score, NumOfMoves, CardIndexOne, CardIndexTwo = 0, 0, 0, -1, -1
    Deck = [x for x in range(8)]*2
    random.shuffle(Deck)
    CardExposed = [False]*16

# 4. Define Event Handlers
def MouseClick(pos):
    global State, Score, CardIndexOne, CardIndexTwo, NumOfMoves
    CardIndex = list(pos)[0]//50
    
    if not CardExposed[CardIndex]:
        if State == 0: 						# turn started
            CardIndexOne = CardIndex
            CardExposed[CardIndex] = True
            State = 1
        elif State == 1: 					# card one flipped
            CardIndexTwo = CardIndex
            CardExposed[CardIndex] = True
            if Deck[CardIndexOne] == Deck[CardIndexTwo]:
                Score += 1
            State = 2
            NumOfMoves += 1
            label.set_text("Moves = " + str(NumOfMoves))
        else: 								# card two flipped
            if Deck[CardIndexOne] != Deck[CardIndexTwo]:
                CardExposed[CardIndexOne], CardExposed[CardIndexTwo] = False, False
                CardIndexOne, CardIndexTwo = -1, -1
            CardIndexOne = CardIndex
            CardExposed[CardIndex] = True
            State = 1  
    
 
def Draw(canvas):							# Card Size 50x100
    for i in range(16):
        if CardExposed[i]:					# Draw Exposed Card With Number
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 1, "Black", "White")
            canvas.draw_text(str(Deck[i]), (i*50+11, 69), 55, "Black")
        else:								# Draw Face Down Card
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 1, "Black", "Red")
    label.set_text("Moves = " + str(NumOfMoves))

Initialize()
# 5. Create a Frame (and add a button and labels)
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", Initialize)
label = frame.add_label("Moves = " + str(NumOfMoves))

# 6. Register Event Handlers
frame.set_mouseclick_handler(MouseClick)
frame.set_draw_handler(Draw)

# 7. Start Frame and Timers
frame.start()