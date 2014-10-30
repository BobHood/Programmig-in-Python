'''
####################################
# Robert Hood                      #
# An Introduction to Interactive   #
#  Programming in Python           #
#                                  #
# Programmign Project              #
#    Stopwatch Game                #
#                                  #
####################################
____________________________________
Mini-project description - "Stopwatch: The Game"

Our mini-project for this week will focus on combining text drawing in the canvas with timers 
to build a simple digital stopwatch that keeps track of the time in tenths of a second. The 
stopwatch should contain "Start", "Stop" and "Reset" buttons. 
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

# template for "Stopwatch: The Game"
import simplegui

# define global variables
CurrentTime = 0
CorrectGuesses = 0
TotalGuesses = 0
Tenths = 0
TimerStopped = False

# define helper function(s)
def format(Time):                       # Create a function to set the proper time format
    global Tenths                       # Pull in the Global for Tenths
    if Time == 0:                       # Set initial time
        return "0:00.0"
    Minutes = int(Time / 600)           # Find Minutes in Time
    Time = Time - (Minutes * 600)       # Remove Minutes from Time remaining
    Seconds = int(Time / 10)            # Find Seconds in Time
    Time = Time - (Seconds * 10)        # Remove Seconds from Time remaining
    Tenths = Time                       # Set Tenths to remaining time
    if (Seconds < 10):                  # Examin whether the player has stopped the timer on 0
        Seconds = "0" + str(Seconds)
    else:
        Seconds = str(Seconds)
    String = str(Minutes) + ":" + Seconds + "." + str(Tenths)
    return String                       # Return Formatted String

# define event handler(s)
def timerstart():                       # Define Button for Start
    global TimerStopped                 # Pull in Global for TimerStopped
    TimerStopped = False                # Set TimerStopped to false (timer is starting)
    Timer.start()                       # Start Timer
    
def timerstop():                        # Define Button for Stop
    global CurrentTime, TimerStopped, TotalGuesses, CorrectGuesses   # Pull in Global(s)
    if CurrentTime % 10 == 0 and TimerStopped == False:  # examine tenths and change guesses variables based on game rules
        CorrectGuesses += 1
        TimerStopped = True
    TotalGuesses += 1
    Timer.stop()
    
def timerreset():                       # Define Button for Reset
    global CurrentTime                       # Pull in Global
    CurrentTime = 0                          # Set CurrentTime to 0
    Timer.stop()                        # Stop timer

def tick():                             # Event for timer increment in tenths
    global CurrentTime
    CurrentTime += 1
    

# define draw handler(s)
def drawtime(canvas):                   # Create a Canvas, Place a Red text timer, with Blue text counters
    canvas.draw_text(format(CurrentTime), (80, 120), 80, "Red")
    canvas.draw_text(str(CorrectGuesses) + " / " + str(TotalGuesses), (200, 40), 40, "Blue")
    
# create frame                          # Create a Frame titled "Stopwatch Game", and set background to White
frame = simplegui.create_frame("Stopwatch Game", 300, 130)
frame.set_canvas_background("white")

# register event handler(s)
frame.set_draw_handler(drawtime)        # Call function to draw the time on the canvas
Timer = simplegui.create_timer(100, tick)       # Create the Timer
Start = frame.add_button("Start", timerstart)   # Create the Start Button
Stop = frame.add_button("Stop", timerstop)      # Create a Stop Button
Reset = frame.add_button("Reset", timerreset)   # Create a Reset Button

# start frame
frame.start()