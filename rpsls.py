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
___________________________________

Mini-project description — Rock-paper-scissors-lizard-Spock
Rock-paper-scissors is a hand game that is played by two people. The players count to three in unison
and simultaneously "throw” one of three hand signals that correspond to rock, paper or scissors. The 
winner is determined by the rules:

Rock smashes scissors
Scissors cuts paper
Paper covers rock
Rock-paper-scissors is a surprisingly popular game that many people play seriously (see the Wikipedia
article for details). Due to the fact that a tie happens around 1/3 of the time, several variants of
Rock-Paper-Scissors exist that include more choices to make ties less likely.

Rock-paper-scissors-lizard-Spock (RPSLS) is a variant of Rock-paper-scissors that allows five choices.
Each choice wins against two other choices, loses against two other choices and ties against itself.
Much of RPSLS's popularity is that it has been featured in 3 episodes of the TV series "The Big Bang Theory". 
The Wikipedia entry for RPSLS gives the complete description of the details of the game.

In our first mini-project, we will build a Python function rpsls(name) that takes as input the string 
name, which is one of "rock", "paper", "scissors", "lizard", or "Spock". The function then simulates 
playing a round of Rock-paper-scissors-lizard-Spock by generating its own random choice from these 
alternatives and then determining the winner using a simple rule that we will next describe.

While Rock-paper-scissor-lizard-Spock has a set of ten rules that logically determine who wins a round 
of RPSLS, coding up these rules would require a large number (5x5=25) of if/elif/else clauses in your 
mini-project code. A simpler method for determining the winner is to assign each of the five choices a number:

0 — rock
1 — Spock
2 — paper
3 — lizard
4 — scissors
In this expanded list, each choice wins against the preceding two choices and loses against the following
two choices (if rock and scissors are thought of as being adjacent using modular arithmetic).

In all of the mini-projects for this class, we will provide a walk through of the steps involved in 
building your project to aid its development. 
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