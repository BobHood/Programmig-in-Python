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
____________________________________

Memory Game Mini-project development process

As usual, we suggest that you start from the program template for this mini-project.

1.  Model the deck of cards used in Memory as a list consisting of 16 numbers with each number lying in 
    the range [0,8) and appearing twice. We suggest that you create this list by concatenating two list 
    with range [0,8) together. Use the Docs to locate the list concatenation operator.
2.  Write a draw handler that iterates through the Memory deck using a for loop and uses draw_text to 
    draw the number associated with each card on the canvas. The result should be a horizontal sequence 
    of evenly-spaced numbers drawn on the canvas.
3.  Shuffle the deck using random.shuffle(). Remember to debug your canvas drawing code before shuffling
    to make debugging easier.
4.  Next, modify the draw handler to either draw a blank green rectangle or the card's value. To implement
    this behavior, we suggest that you create a second list called exposed. In the exposed list, the ith
    entry should be True if the ith card is face up and its value is visible or False if the ith card 
    is face down and it's value is hidden. We suggest that you initialize exposed to some known values 
    while testing your drawing code with this modification.
5.  Now, add functionality to determine which card you have clicked on with your mouse. Add an event handler
    for mouse clicks that takes the position of the mouse click and prints the index of the card that you 
    have clicked on to the console. To make determining which card you have clicked on easy, we suggest 
    sizing the canvas so that the sequence of cards entirely fills the canvas.
6.  Modify the event handler for mouse clicks to flip cards based on the location of the mouse click. If 
    the player clicked on the ith card, you can change the value of exposed[i] from False to True. If the 
    card is already exposed, you should ignore the mouseclick. At this point, the basic infrastructure for 
    Memory is done.
7.  You now need to add game logic to the mouse click handler for selecting two cards and determining if 
    they match. We suggest following the game logic in the example code discussed in the Memory video. 
    State 0 corresponds to the start of the game. In state 0, if you click on a card, that card is exposed,
    and you switch to state 1. State 1 corresponds to a single exposed unpaired card. In state 1, if you 
    click on an unexposed card, that card is exposed and you switch to state 2. State 2 corresponds to the 
    end of a turn. In state 2, if you click on an unexposed card, that card is exposed and you switch to 
    state 1.
8.  Note that in state 2, you also have to determine if the previous two cards are paired or unpaired. If 
    they are unpaired, you have to flip them back over so that they are hidden before moving to state 1. We 
    suggest that you use two global variables to store the index of each of the two cards that were clicked 
    in the previous turn.
9.  Add a counter that keeps track of the number of turns and uses set_text to update this counter as a label 
    in the control panel. (BTW, Joe's record is 12 turns.)  This counter should be incremented after either 
    the first or second card is flipped during a turn.
10. Finally, implement the new_game() function (if you have not already) so that the "Reset" button reshuffles
    the cards, resets the turn counter and restarts the game. All cards should start the game hidden.
11. (Optional) You may replace the draw_text for each card by a draw_image that uses one of eight different 
    images.

Once the run button is clicked in CodeSkulptor, the game should start. You should not have to hit the 
"Reset" button to start. Once the game is over, you should hit the "Reset" button to restart the game. 
While this project may seem daunting at first glance, our full implementation took well under 100 
lines with comments and spaces. If you feel a little bit intimidated, focus on developing your project 
to step six. Our experience is that, at this point, you will begin to see your game come together and 
the going will get much easier.
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
0. Import Python Modules
1. Globals (states)
2. Helper Functions
3. Classes (N/A)
4. Define Event Handlers
5. Create a Frame
6. register Event Handlers (N/A)
7. start frame and timers

Code Start
____________________________________
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