'''
####################################
# Robert Hood                      #
# An Introduction to Interactive   #
#  Programming in Python           #
#                                  #
# Programmign Project              #
#    RiceRocks                     #
#                                  #
####################################

Mini-project description - RiceRocks (Asteroids)
For our last mini-project, we will complete the implementation of RiceRocks, 
an updated version of Asteroids,  that we began last week.  You may start with 
either your code or the program template which includes a full implementation 
of Spaceship and will be released immediately after the deadline for the Spaceship 
mini-project (by making the preceding link live).  If you start with your own code, 
you should add the splash screen image that you dismiss with a mouse click before 
starting this mini-project.  We strongly recommend using Chrome for this mini-project 
since Chrome's superior performance will become apparent when your program 
attempts to draw dozens of sprites.
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
time = 0
GameStarted = False

Rocks = 12
StartingLives = 3
MaxRocks = 12
RockVelocityFactorIncrease = 0.05
AngularVelocity = 0.1
ShipThrustVelocity = 0.2
FrictionFactor = 0.99

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
# soundtrack courtesty of by Eric Matyas@soundimage.org, used with permission
soundtrack = simplegui.load_sound("https://dl.dropbox.com/s/1k6gdv3rz4am5si/Dystopic-Dreamscape.mp3")
# Missle sound courtesy of Freesfx.co.uk used with permission
missile_sound = simplegui.load_sound("https://dl.dropbox.com/s/ff25a8n4rmfaths/science_fiction_laser_005.mp3")
missile_sound.set_volume(.5)
# Thrust assest purchased from sounddogs.com, please do not redistribute
ship_thrust_sound = simplegui.load_sound("https://dl.dropbox.com/s/poc3sffxdtc39xs/thrust.mp3")
# Explosion courtesy of Mike Koenig @ Sound-Bible used with permission
explosion_sound = simplegui.load_sound("https://dl.dropbox.com/s/2yn6813li8dncop/Grenade_Explosion-SoundBible.com-2100581469.mp3")
explosion_sound.set_volume(.3)

# 2. Helper Functions
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# 3. Classes
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] 
                            + self.image_size[0], self.image_center[1]],
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
    
    def update(self):
            # update angle
        self.angle += self.angle_vel
            
            # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
            # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * ShipThrustVelocity
            self.vel[1] += acc[1] * ShipThrustVelocity
        
        self.vel[0] *= FrictionFactor
        self.vel[1] *= FrictionFactor
    
    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def increment_angle_vel(self):
        self.angle_vel += AngularVelocity
    
    def decrement_angle_vel(self):
        self.angle_vel -= AngularVelocity
    
    def shoot(self):
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] 
                    + self.radius 
                    * forward[0], self.pos[1] 
                    + self.radius 
                    * forward[1]]
        missile_vel = [self.vel[0] 
                    + 6 * forward[0], self.vel[1] 
                    + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        MissleGroup.add(a_missile)

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
        if self.animated:
            self.image_center = [64 + 128 * self.age, 64]
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
            # update angle
        self.angle += self.angle_vel
        
            # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
            # update age
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        if (dist(self.get_position(), other_object.get_position()) < (self.get_radius() + other_object.get_radius())):
            return True
        else:
            return False

#4. Define Event Handlers
            # key handlers to control ship
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        PlayerShip.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        PlayerShip.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        PlayerShip.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        PlayerShip.shoot()

def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        PlayerShip.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        PlayerShip.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        PlayerShip.set_thrust(False)

            # mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global GameStarted, Rocks, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not GameStarted) and inwidth and inheight:
        GameStarted = True
        Rocks = MaxRocks
        lives = StartingLives
        score = 0
        soundtrack.rewind()
        soundtrack.play()

def draw(canvas):
    global time, GameStarted, lives, score, Rocks, RockGroup
    
            # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
            # draw UI
    canvas.draw_text("Lives: " + str(lives), (WIDTH * 0.10, HEIGHT * 0.05), 20, 'Lime', 'monospace')
    canvas.draw_text("Score: " + str(score), (WIDTH * 0.75, HEIGHT * 0.05), 20, 'Lime', 'monospace')

            # draw ship and sprites
    PlayerShip.draw(canvas)
    process_sprite_group(RockGroup, canvas)
    process_sprite_group(MissleGroup, canvas)
    process_sprite_group(ExplosionGroup, canvas)
    
            # update ship and sprites
    PlayerShip.update()
    
            # determine collisions
    if group_collide(RockGroup, PlayerShip):
        lives -= 1
        if lives <= 0:
            GameStarted = False
    
    score += group_group_collide(MissleGroup, RockGroup)
    
            # draw splash screen if not GameStarted
    if not GameStarted:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        Rocks = 0
        RockGroup = set()
        soundtrack.pause()

            # timer handler that spawns a rock
def rock_spawner():
    if len(RockGroup) < Rocks:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        #rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        rock_vel = [random.random() * (.6 + RockVelocityFactorIncrease * score) - (.3 + RockVelocityFactorIncrease * score), random.random() * (.6 + RockVelocityFactorIncrease * score) - (.3 + RockVelocityFactorIncrease * score)]
        rock_avel = random.random() * .2 - .1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        if a_rock.collide(PlayerShip):
            rock_spawner()
        else:
            RockGroup.add(a_rock)

            # take a set and a canvas and call the update and draw methods for each sprite in the group
def process_sprite_group(sprite_group, canvas):
    for sprite in set(sprite_group):
        sprite.draw(canvas)
        if sprite.update():
            sprite_group.remove(sprite)

            # take a set group and an a sprite other_object and check for collisions between other_object and elements of the group
def group_collide(group, other_object):
    for sprite in set(group):
        if sprite.collide(other_object):
            an_explosion = Sprite(sprite.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            ExplosionGroup.add(an_explosion)
            group.remove(sprite)
            return True
    return False

            # return the number of elements in the first group that collide with the second group as well as delete these elements in the first group
def group_group_collide(first_group, second_group):
    collide_count = 0
    for element in set(first_group):
        if group_collide(second_group, element):
            collide_count += 1
            first_group.discard(element)
    return collide_count

# 5. Create a Frame (and initialize sprites)
frame = simplegui.create_frame("RiceRocks", WIDTH, HEIGHT)
PlayerShip = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
RockGroup = set()
MissleGroup = set()
ExplosionGroup = set()


# 6. register Event Handler(s)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(1000.0, rock_spawner)


# 7. start frame and timer(s)
timer.start()
frame.start()