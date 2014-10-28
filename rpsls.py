'''
####################################
# Robert Hood                      #
# An Introduction to Interactive   #
#  Programming in Python           #
#                                  #
# Programmign Project              #
#  Rock-Paper-Sisors-Lizzard-Spock #
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

The key idea of this program is to equate the strings
"rock", "paper", "scissors", "lizard", "Spock" to numbers
as follows:
0 - rock
1 - Spock
2 - paper
3 - lizard
4 - scissors

Code Start
'''

# helper functions
import random
def name_to_number(name):
    if name == "rock":
        number = 0
        return number
    elif name == "Spock":
        number = 1
        return number
    elif name == "paper":
        number = 2
        return number
    elif name == "lizard":
        number = 3
        return number
    elif name == "scissors":
        number = 4
        return number
def number_to_name(number):
    if number == 0:
        name = "rock"
        return name
    elif number == 1:
        name = "Spock"
        return name
    elif number == 2:
        name = "paper"
        return name
    elif number == 3:
        name = "lizard"
        return name
    elif number == 4:
        name = "scissors"
        return name
def rpsls(player_choice):
    player_number = name_to_number(player_choice)
    print "Player chooses", player_choice
    computer_number = random.randrange(0,5)
    print "Computer chooses", number_to_name(computer_number)
    difference = (player_number - computer_number) % 5
    if difference == 3 or difference == 4:
        print "Computer wins!\n"
        return
    elif difference == 1 or difference == 2:
        print "Player wins!\n"
        return
    elif difference == 0:
        print "Player and Computer tie!\n"
        return
    else:
        print "Error, function drops out"
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
# always remember to check your completed program against the grading rubric