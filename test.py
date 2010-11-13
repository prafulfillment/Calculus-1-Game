# experiments with module pygame
# free from: http://www.pygame.org/
# move a rectangle with an image in it
# if you have the image of a ball, you have a bouncing ball
# tested with Python24 and Pygame171    vegaseat   02feb2007

import pygame as pg

# initialize pygame
pg.init()

# download the image from: 
# http://www.daniweb.com/techtalkforums/post310029-97.html
# or use an image you have (.bmp  .jpg  .png  .gif)
# ideally the image should have a black background or
# you have to fill the screen with the matching background
image_file = "ball_r.gif"

# image moves [x, y] at a time
# you can change trajectory, speed and direction
im_dir = [2, 1]

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

# the event loop also loops the animation code
while True:
    pg.event.pump()
    keyinput = pg.key.get_pressed()
    # exit on corner 'x' click or escape key press
    if keyinput[pg.K_ESCAPE] or pg.event.peek(pg.QUIT):
        raise SystemExit

    # set the move
    im_rect = im_rect.move(im_dir)
    # detect the boundaries and change directions
    # left/right boundaries are 0 to sreen width
    if im_rect.left < 0 or im_rect.right > sw:
        im_dir[0] = -im_dir[0]
    # top/bottom boundaries are 0 to screen height
    if im_rect.top < 0 or im_rect.bottom > sh:
        im_dir[1] = -im_dir[1]
    # this erases the old sreen with black
    screen.fill(black)
    # put the image on the screen
    screen.blit(image, im_rect)
    # update screen
    pg.display.flip()
