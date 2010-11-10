import os
import pygame
from pygame.locals import *

def load_image(*path):
  image = pygame.image.load(os.path.join(os.getcwd(), 'data', *path)).convert()
  return image

class Camera(object):
  def __init__(self):
    self.pos = 0, 0
  
  def getpos(self):
    return self.pos
  
  def move(self, delta):
    self.pos = self.pos[0] + delta[0], self.pos[1] + delta[1]
  
  def moveto(self, newpos):
    self.pos = newpos

class House(pygame.sprite.Sprite):
  def __init__(self, skin):
    pygame.sprite.Sprite.__init__(self)
    self.image = load_image('houses', skin, 'house.png')
    self.rect = self.image.get_rect()
    self.realrect = self.rect
  
  def move_to(self, pos):
    self.realrect = pygame.Rect(pos, self.realrect.size)
  
  def update(self, camera):
    #self.move_to((self.rect.left, self.rect.top + 1))
    self.rect = self.rect.move((0, 1))
    self.rect = self.realrect.move((-camera.getpos()[0], -camera.getpos()[1]))

WIDTH = 800
HEIGHT = 600
AREA_SIZE = 1600, 600
FPS = 60

camera = Camera()

height_offset = 400
left_offset = 20

house_skin = 'default'
bg_skin = 'default'
catapult_skin = 'default'

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

houses = House(house_skin), House(house_skin)
background = load_image('backgrounds', bg_skin, 'bg.png')

houses[0].realrect.left = left_offset
houses[0].realrect.bottom = height_offset
houses[1].realrect.right = AREA_SIZE[0] - left_offset
houses[1].realrect.bottom = height_offset

allsprites = pygame.sprite.RenderPlain(houses)

running = True

while running :
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      break
    #elif event.type == KEY_DOWN:
    #  running = False
    #  break
  
  #camera.move((1, 0))
  
  screen.blit(background, [-i for i in camera.getpos()])
  
  allsprites.update(camera)
  allsprites.draw(screen)
  pygame.display.flip()
  clock.tick(FPS)