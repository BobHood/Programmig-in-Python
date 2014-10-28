'''
####################################
# Robert Hood                      #
# An Introduction to Interactive   #
#  Programming in Python           #
#                                  #
# Programmign Project              #
#    Guess the Number              #
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

Code Start
'''

# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui            # Importing the GUI module
import random               # Import the Random Module
import math                 # Import the Math module

# initialize global variables used in your code here

SecretNumber = 0            # Initilize the number the player is trying to guess to 0
Count = 0                   # Initilize the guess count to 0
MaxCount = 0                # Initilize the maximum guess possible count to 0


# define event handlers for control panel
def Range100():             # This function sets the range of the game to 0 - 100 and initiates the game
    print "You have chosen the 0 - 100 game mode.\n Make your guess.." 
    global SecretNumber, MaxCount, Count                     # Pull the Global Varibles into the function
    SecretNumber = random.randrange(0, 100)                  # Set the secret number to a random number between 0-100
    Count = 0               # Set count to 0
    MaxCount = 7            # Set MaxCount to 7, the maximum ammount to guarentee a win in 0-100

def Range1000():            # This function sets the range of the game to 0 - 1000 and initiates the game
    print "You have chosen the 0 - 1000 game mode.\n Make your guess.."
    global SecretNumber, MaxCount, Count                     # Pull the Global Varibles into the function
    SecretNumber = random.randrange(0, 1000)                 # Set the secret number to a random number between 0-1000
    Count = 0               # Set count to 0
    MaxCount = 10           # Set MaxCount to 10, the maximum ammount to guarentee a win in 0-1000
    
def InputGuess(guess):      # this is the games Main logic Function
    global Count            # Pull the Global Varible into the function
    Count += 1              # Increment the count by one
    print "You've guessed: ", guess, "You have had", Count, "guesses so far of", MaxCount, "possible guesses\n"
    if int(guess) > SecretNumber:                            # Evaluate the guess to the secret number
        print "My number is Lower. Guess again"              # Provide Feedback Lower
    elif int(guess) < SecretNumber:
        print "My number is Higher. Guess again"             # Provide Feedback Higher
    else:
        print "You are Correct!!\n Starting new game...\n"   # Provide Feedback Correct
        Count = 0           # Set Count back to 0
        return
    if Count >= MaxCount:
        print "Maximum number of guesses used.\n Restarting." # Provide feedback Faild to guess
        Count = 0           # Set Count back to 0
        return
    
# create frame
frame = simplegui.create_frame("Guess My Number", 0, 150)

# register event handlers for control elements and start frame
frame.add_button("0 - 100", Range100, 80)                   # Create button for 0-100 game, width 80
frame.add_button("0 - 1000", Range1000, 80)                 # Create button for 0-1000 game, width 80
frame.add_input("Your Guess", InputGuess, 80)               # Create input field for player guess, width 80


# Start Frame
frame.start()               # Start the frame window