'''
####################################
# Robert Hood                      #
# An Introduction to Interactive   #
#  Programming in Python           #
#                                  #
# Programmign Project              #
#    Spaceship                     #
#                                  #
####################################

Mini-project description - Spaceship
In our last two mini-projects, we will build a 2D space game RiceRocks that is inspired by 
the classic arcade game Asteroids (1979). Asteroids is a relatively simple game by today's 
standards, but was still immensely popular during its time. (Joe spent countless quarters 
playing it.) In the game, the player controls a spaceship via four buttons: two buttons 
that rotate the spaceship clockwise or counterclockwise (independent of its current velocity), 
a thrust button that accelerates the ship in its forward direction and a fire button that 
shoots missiles. Large asteroids spawn randomly on the screen with random velocities. The 
player's goal is to destroy these asteroids before they strike the player's ship. In the 
arcade version, a large rock hit by a missile split into several fast moving small asteroids 
that themselves must be destroyed. Occasionally, a flying saucer also crosses the screen and 
attempts to destroy the player's spaceship. Searching for "asteroids arcade" yields links to 
multiple versions of Asteroids that are available on the web (including an updated version by 
Atari, the original creator of Asteroids).
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
1. Globals (states) and Artwork
2. Helper Functions
3. Classes
4. Define Event Handlers
5. Create a Frame (and initialize sprites)
6. register Event Handlers
7. start frame and timers

Code Start
____________________________________
'''

# 0. Import Python Modules
import simplegui
import math
import random

# 1. Globals (states) and Artwork
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

AngularVelocity = 0.1
Friction = 0.99
Acceleration = 0.2
MissleVelocity = 8

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("https://www.dropbox.com/s/m6pu5ofdek3az9q/debris2_blue.png?dl=1")
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("https://www.dropbox.com/s/edqz8u17ycw89ea/nebula_blue.f2014.png?dl=1")
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("https://www.dropbox.com/s/5bltmhnvl7jfms3/splash.png?dl=1")
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("https://www.dropbox.com/s/0l8oelrvwzr5n2d/double_ship.png?dl=1")
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("https://www.dropbox.com/s/s9ivkvuw7bpiwu1/shot2.png?dl=1")
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("https://www.dropbox.com/s/ow9hc264qdel9hn/asteroid_blue.png?dl=1")
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("https://www.dropbox.com/s/ypg8qeelne1lryt/explosion_alpha.png?dl=1")
# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# 2. Helper Functions
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# 3. Classes
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = angle
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        canvas.draw_image(self.image, ship_info.get_center(), ship_info.get_size(), self.pos, ship_info.get_size(), self.angle)

    def update(self):
        if self.thrust:
            PlayerShip.image_center[0] = 45 + 90
            self.vel[0] += angle_to_vector(self.angle)[0] * Acceleration
            self.vel[1] += angle_to_vector(self.angle)[1] * Acceleration
        else:
            PlayerShip.image_center[0] = 45

        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        self.vel[0] *= Friction
        self.vel[1] *= Friction

        self.angle += self.angle_vel

    def thrusters_on(self, ThrustEngaged):
        if ThrustEngaged:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            ship_thrust_sound.pause()

    def shoot(self):
        global MissleOnScreen
        MissleOnScreen = Sprite([self.pos[0] 
                        + angle_to_vector(self.angle)[0] 
                        * self.radius, self.pos[1] 
                        + angle_to_vector(self.angle)[1] 
                        * self.radius], [self.vel[0] 
                        + angle_to_vector(self.angle)[0] 
                        * MissleVelocity, self.vel[1] 
                        + angle_to_vector(self.angle)[1] 
                        * MissleVelocity], 0, 0, missile_image, missile_info, missile_sound)

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel

#4. Define Event Handlers
def draw(canvas):
    global time, score, lives

    # Animiate Background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    canvas.draw_text("Lives: " + str(lives), (WIDTH * 0.10, HEIGHT * 0.05), 20, 'Green', 'monospace')
    canvas.draw_text("Score: " + str(score), (WIDTH * 0.75, HEIGHT * 0.05), 20, 'Green', 'monospace')

    PlayerShip.draw(canvas)                             # Draw PlayerShip sprite
    BigRock.draw(canvas)                                # Draw BigRock sprite
    MissleOnScreen.draw(canvas)                         # Draw Missle sprites

    PlayerShip.update()                                 # Update PlayerShip sprite
    BigRock.update()                                    # Update BigRock sprite
    MissleOnScreen.update()                             # Update Missle sprites


def rock_spawner():                                     # timer handler that spawns a rock
    global BigRock
    BigRock = Sprite([random.randrange(800), random.randrange(600)], [-0.5 + random.random(), -0.5 + random.random()], 2 * math.pi * random.random(), (-0.5 + random.random()) / 5, asteroid_image, asteroid_info)

def keydown(key):                                       # Key Down Checking function
    if key == simplegui.KEY_MAP["up"]:
        PlayerShip.thrust = True
        PlayerShip.thrusters_on(True)
    elif key == simplegui.KEY_MAP["space"]:
        PlayerShip.shoot()
    if key == simplegui.KEY_MAP["left"]:
        PlayerShip.angle_vel = -AngularVelocity
    elif key == simplegui.KEY_MAP["right"]:
        PlayerShip.angle_vel = AngularVelocity

def keyup(key):                                         # Key Up Checking function
    if key == simplegui.KEY_MAP["up"]:
        PlayerShip.thrust = False
        PlayerShip.thrusters_on(False)
    if key == simplegui.KEY_MAP["left"]:
        PlayerShip.angle_vel = 0
    elif key == simplegui.KEY_MAP["right"]:
        PlayerShip.angle_vel = 0

# 5. Create a Frame (and initialize sprites)
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
        # initialize PlayerShip, BigRock and Missle sprites
PlayerShip = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
BigRock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
MissleOnScreen = Sprite([-10,-10], [0,0], 0, 0, missile_image, missile_info)

# 6. register Event Handler(s)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# 7. start frame and timer(s)
timer.start()
frame.start()
