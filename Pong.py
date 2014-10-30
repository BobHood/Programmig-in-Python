'''
####################################
# Robert Hood                      #
# An Introduction to Interactive   #
#  Programming in Python           #
#                                  #
# Programmign Project              #
#    Pong                          #
#                                  #
####################################

____________________________________

Mini-project #4 - "Pong"
In this project, we will build a version of Pong, one of the first arcade video games (1972). 
While Pong is not particularly exciting compared to today's video games, Pong is relatively 
simple to build and provides a nice opportunity to work on the skills that you will need to 
build a game like Asteroids. As usual, we have provided a program template that can be used 
to guide your development of Pong.
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

# 1. initialize global(s)

Width = 600                                 # Game Field Width
Height = 400                                # Game Field Height
BallRadius = 20                             # Set "Size" of the ball
PaddleWidth = 8                             # Set the Paddle Width
PaddleHeight = 80                           # Set the Paddle Height
HalfPaddleWidth = PaddleWidth / 2           # Set Half the Paddle Width
HalfPaddleHeight = PaddleHeight / 2         # Set Half the Paddle Height
BallPosition = [300, 200]                   # Set Ball Start Position (List Variable [x,y])
BallVelocity = [0, 0]                       # Set Ball Start Velocity (List Variable)
BallStarted = False                         # Set Ball started
PointRight = False                          # Set Ball vectoring right
PointLeft = False                           # Set Ball vectorign left
PointsToTheRight = 0                        # Set Ball points right
PointsToTheLeft = 0                         # Set ball points left
PaddleOnePosition = [Width - 1 - PaddleWidth/2, Height/2 - 1] #Paddle One positioning
PaddleTwoPosition = [PaddleWidth/2, Height/2 -1] #Paddle Two Positioning
PaddleOneVelocity = [0, 0]                  # Paddle One Velocity
PaddleTwoVelocity = [0, 0]                  # Paddle Two velocity

# 2. helper function(s)

def BallInitiation(right):                  # Spawn Ball
    global BallPosition, BallVelocity, BallStarted
    if right == True:
        BallPosition = [Width/2, Height/2]
        BallVelocity = [3, 3]
    else:
        BallPosition = [Width/2, Height/2]
        BallVelocity = [-3, 3]
    BallStarted = True    
    
def update_ball():                          # Ball's position and velocity vector
    global BallPosition, BallVelocity
    check_for_collisions()
    BallPosition = [BallPosition[0] + BallVelocity[0], BallPosition[1] - BallVelocity[1]]

def check_for_collisions():                 # Check for ball position on the paddle and modify the velocity based on position of impact
    global BallRadius, BallPosition, BallVelocity, PaddleOnePosition, PaddleTwoPosition, PointRight, PointLeft
                                            # Check the left paddle
    if BallPosition[0] - BallRadius <= PaddleWidth and BallPosition[1] > PaddleOnePosition[1] - HalfPaddleHeight and BallPosition[1] < PaddleOnePosition[1] + HalfPaddleHeight:
        BallVelocity[0] *= -1.1
                                            # Check the right paddle
    if BallPosition[0] + BallRadius >= Width - 1 -PaddleWidth and BallPosition[1] > PaddleTwoPosition[1] - HalfPaddleHeight and BallPosition[1] < PaddleTwoPosition[1] + HalfPaddleHeight: 
        BallVelocity[0] *= -1.1
                                            # Check the celling
    if BallPosition[1] + BallRadius >= Height -1:
        BallVelocity[1] *= -1
                                            # Check floor
    if BallPosition[1] - BallRadius <= 0:
        BallVelocity[1] *= -1 
                                            # Point for right Player
    if BallPosition[0] < 0:
        PointRight = True
                                            # Point for left Player
    if BallPosition[0] > Width:
        PointLeft = True

def UpdatePaddleOne():                      # Update Paddle Position For Paddle One
    PaddleOnePosition[1] += PaddleOneVelocity[1]
    if PaddleOnePosition[1] - HalfPaddleHeight <= 0:
        PaddleOnePosition[1] = HalfPaddleHeight
    if PaddleOnePosition[1] + HalfPaddleHeight >= Height - 1:
        PaddleOnePosition[1] = Height - 1 - HalfPaddleHeight
        
def UpdatePaddleTwo():                      # Update Paddle Position For Paddle Two
    PaddleTwoPosition[1] += PaddleTwoVelocity[1]
    if PaddleTwoPosition[1] - HalfPaddleHeight <= 0:
        PaddleTwoPosition[1] = HalfPaddleHeight
    if PaddleTwoPosition[1] + HalfPaddleHeight >= Height - 1:
        PaddleTwoPosition[1] = Height - 1 - HalfPaddleHeight

# 4. define event handlers

def CreateNewGame():
    global PaddleOnePosition, PaddleTwoPosition, PaddleOneVelocity, PaddleTwoVelocity
    global score1, score2  

def DrawElements(c):
    global score1, score2, PaddleOnePosition, PaddleTwoPosition, BallPosition, BallVelocity
    global BallStarted, PointLeft, PointRight, PointsToTheLeft, PointsToTheRight
                                            # Update paddle(s) vertical position, set limits to keep paddle on the screen
    UpdatePaddleOne()
    UpdatePaddleTwo()    
                                            # draw mid field line and gutter Lines
    c.draw_line([Width / 2, 0],[Width / 2, Height], 2, "Black")
    c.draw_line([PaddleWidth, 0],[PaddleWidth, Height], 1, "Black")
    c.draw_line([Width - PaddleWidth, 0],[Width - PaddleWidth, Height], 1, "Black")
                                            # draw paddles
    c.draw_polygon([(0, PaddleOnePosition[1] + HalfPaddleHeight), (0,PaddleOnePosition[1] - HalfPaddleHeight), (PaddleWidth, PaddleOnePosition[1] - HalfPaddleHeight), (PaddleWidth, PaddleOnePosition[1] + HalfPaddleHeight)], 1, "Red", "Green")
    c.draw_polygon([(Width-1, PaddleTwoPosition[1] + HalfPaddleHeight), (Width-1,PaddleTwoPosition[1] - HalfPaddleHeight), (Width - 1 - PaddleWidth, PaddleTwoPosition[1] - HalfPaddleHeight), (Width - 1 - PaddleWidth, PaddleTwoPosition[1] + HalfPaddleHeight)], 1, "Blue", "Green")
                                            # update start position and random velocity for ball
    if BallStarted == False:
        BallInitiation(random.choice([True, False]))
    update_ball()
                                            # draw ball and scores
    if PointLeft == True:
        PointLeft = False
        PointsToTheLeft += 1
        BallStarted = False
    if PointRight == True:
        PointRight = False
        PointsToTheRight += 1
        BallStarted = False  
    c.draw_circle(BallPosition, BallRadius, 2, "Blue", "Red")
    c.draw_text(str(PointsToTheLeft), (Width/3, Height/3), 60, "Red")
    c.draw_text(str(PointsToTheRight), (2*Width/3, Height/3), 60, "Red")

def KeyDepressed(key):                      # Check for key depressed to move paddles
    global PaddleOneVelocity, PaddleTwoVelocity, PaddleOnePosition, PaddleTwoPosition
    if key == simplegui.KEY_MAP['s']:
        PaddleOneVelocity[1] = 5
    elif key == simplegui.KEY_MAP['w']:
        PaddleOneVelocity[1] = -5
    if key==simplegui.KEY_MAP['up']:
        PaddleTwoVelocity[1] = -5
    elif key==simplegui.KEY_MAP['down']:
        PaddleTwoVelocity[1] = 5
    
        
def KeyReleased(key):                       # Check for key release to stop moving paddles
    global PaddleOneVelocity, PaddleTwoVelocity, PaddleOnePosition, PaddleTwoPosition
    if key == simplegui.KEY_MAP['s']:
        PaddleOneVelocity[1] = 0
    elif key == simplegui.KEY_MAP['w']:
        PaddleOneVelocity[1] = 0
    if key==simplegui.KEY_MAP["up"]:
        PaddleTwoVelocity[1] = 0
    elif key==simplegui.KEY_MAP["down"]:
        PaddleTwoVelocity[1] = 0

def ResetGame():                            # Reset game to 0 | 0 and start ball from center with random vector
    global BallStarted, PointRight, PointLeft, PointsToTheRight, PointsToTheLeft
    BallStarted = False
    PointRight = False
    PointLeft = False
    PointsToTheRight = 0
    PointsToTheLeft = 0
    BallInitiation(random.choice([True, False]))

# 5. create frame

frame = simplegui.create_frame("The Game of Pong", Width, Height)
frame.set_canvas_background("White")
frame.set_draw_handler(DrawElements)
frame.set_keydown_handler(KeyDepressed)
frame.set_keyup_handler(KeyReleased)
button1 = frame.add_button("Reset", ResetGame)


# 7. start frame
frame.start()