# experiments with module pygame
# free from: http://www.pygame.org/
# move a rectangle with an image in it
# if you have the image of a ball, you have a bouncing ball
# tested with Python24 and Pygame171    vegaseat   02feb2007

import pygame as pg
import math

# initialize pygame
pg.init()

# download the image from: 
# http://www.daniweb.com/techtalkforums/post310029-97.html
# or use an image you have (.bmp  .jpg  .png  .gif)
# ideally the image should have a black background or
# you have to fill the screen with the matching background
image_file = "ball_r.gif"

# RGB color tuple for screen background
black = (0,0,0)
# screen width and height
sw = 640
sh = 480
# create a screen
screen = pg.display.set_mode((sw, sh))
# give the screen a title
pg.display.set_caption('bouncing image (press escape to exit)')

try:
    # load an image
    # convert() unifies the pixel format for faster blit
    image = pg.image.load(image_file).convert()

except:
    print "Please supply image file %s" % image_file
    raise SystemExit

# get the rectangle the image occupies
im_rect = image.get_rect()
im_rect[1] = sh - image.get_width()

# the event loop also loops the animation code
tx = 0
ty = 0
a = math.pi/4
g = 9.81
v = 100
vx = v * math.cos(a)
vy = v * math.sin(a)
while True:
    pg.event.pump()
    keyinput = pg.key.get_pressed()
    # exit on corner 'x' click or escape key press
    if keyinput[pg.K_ESCAPE] or pg.event.peek(pg.QUIT):
        raise SystemExit    

    screen.fill(black)
    # put the image on the screen

    tx = tx + .1

    x = vx*tx

    y = (-vy*ty + (g * ty**2)) + (sh - image.get_height())
    
    if y > sh - image.get_height():
        vy = vy * .9
        ty = 0.0
        y = sh - image.get_height()
    else:
        ty = ty + 0.1
    

    if x < sw + image.get_width():
        im_rect[0] = x
        im_rect[1] = y
        print "x,y = ",x, y


    screen.blit(image, im_rect)
    # update screen
    pg.display.flip()
