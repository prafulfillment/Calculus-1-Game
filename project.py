import os
import pygame
from pygame.locals import *
import graphics

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


height_offset = 400
left_offset = 20

house_skin = 'default'
bg_skin = 'default'
catapult_skin = 'default'

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

class Screen(object):
  def __init__(self):
    pass
  
  def update(self):
    pass
  
  def draw(self, screen):
    pass

class GameScreen(object):
  def __init__(self, house_skin, bg_skin, catapult_skin):
    self.houses = House(house_skin), House(house_skin)
    self.background = load_image('backgrounds', bg_skin, 'bg.png')
    
    self.houses[0].realrect.left = left_offset
    self.houses[0].realrect.bottom = height_offset
    self.houses[1].realrect.right = AREA_SIZE[0] - left_offset
    self.houses[1].realrect.bottom = height_offset
    self.camera = Camera()
    
    self.sprites = pygame.sprite.RenderPlain(self.houses)
  
  def update(self):
    self.sprites.update(self.camera)
  
  def draw(self, screen):
    screen.blit(self.background, [-i for i in self.camera.getpos()])
    self.sprites.draw(screen)
  
  def reset(self):
    pass
  
  def keydown(self, event):
    pass
  
  def keyup(self, event):
    pass
  
  def mousemotion(self, event):
    pass
  
  def mousedown(self, event):
    pass
  
  def mouseup(self, event):
    pass

class Button(object):
  def __init__(self, rect, caption):
    self.rect = rect
    self.caption = caption
    self.selected = False
    self.mouseisdown = False
    self.onclick = lambda: None
  
  def draw(self, screen):
    color = (255, 225, 225) if self.selected else (192, 192, 192)
    if self.mouseisdown:
      color = (96, 96, 96)
    
    pygame.draw.rect(screen, color, self.rect)
    pygame.draw.rect(screen, (128, 128, 128), self.rect, 1)
    renderedText = graphics.Graphics.renderText(self.caption)
    screen.blit(renderedText, (self.rect.left + self.rect.width / 2. - renderedText.get_rect().width / 2., self.rect.top + self.rect.height / 2. - renderedText.get_rect().height / 2.))
  
  def mousemotion(self, event):
    pass
  
  def mousedown(self, event):
    self.mouseisdown = True
  
  def mouseup(self, event):
    self.mouseisdown = False
    self.onclick()
  
  def mousecancel(self):
    self.mouseisdown = False

class OptionScreen(object):
  def __init__(self, options, buttoncaption, donehandler=lambda x:None):
    global WIDTH, HEIGHT
    
    self.options = options
    self.button = buttoncaption
    self.selected = 0
    self.lastmouse = (0,0)
    self.donehandler = donehandler
    
    self.buttons = []
    buttonhperc = 0.75
    
    real_button_height = HEIGHT/ (len(self.options) + 1)
    def getbuttonmetrics(real_button_height, buttonhperc, idx):
      button_voffset = real_button_height * idx + real_button_height * .25 * .5
      button_height = real_button_height * 0.75
      button_hoffset = WIDTH * (1 - buttonhperc) * 0.5
      button_width = WIDTH * buttonhperc
      return pygame.Rect(button_hoffset, button_voffset, button_width, button_height)
    
    
    for idx, option in enumerate(self.options + [buttoncaption]):
      if idx == len(self.options):
        button = Button(getbuttonmetrics(real_button_height, 0.5, idx), option)
        def donebutton(button=button):
          for i, b in enumerate(self.buttons):
            if b.selected:
              self.donehandler(i)
        button.onclick = donebutton
      else:
        button = Button(getbuttonmetrics(real_button_height, buttonhperc, idx), option)
        def select_this_button(self=self, button=button):
          for b in self.buttons:
            if b == button:
              button.selected = True
            else:
              b.selected = False
        button.onclick = select_this_button
      self.buttons.append(button)
  
  def update(self):
    pass
  
  def draw(self, screen):
    for button in self.buttons:
      button.draw(screen)
      
  
  def reset(self):
    pass
  
  def keydown(self, event):
    pass
  
  def keyup(self, event):
    pass
  
  def mousemotion(self, event):
    for button in self.buttons:
      if button.rect.collidepoint(event.pos):
        button.mousemotion(event)
  
  def mousedown(self, event):
    for button in self.buttons:
      if button.rect.collidepoint(event.pos):
        button.mousedown(event)
  
  def mouseup(self, event):
    for button in self.buttons:
      if button.rect.collidepoint(event.pos):
        button.mouseup(event)
      else:
        button.mousecancel()


class GameOverScreen(object):
  def __init__(self, retryclick):
    global WIDTH, HEIGHT
    self.button = Button(pygame.Rect(WIDTH / 2. - 100, HEIGHT - 200, 200, 100), 'Retry')
    self.button.onclick = retryclick
  
  def update(self):
    pass
  
  def draw(self, screen):
    text = graphics.Graphics.renderText('\\s(26)Game Over')
    screen.blit(text, (screen.get_rect().width / 2. - text.get_rect().width / 2,
                       screen.get_rect().height / 2. - text.get_rect().height / 2))
    self.button.draw(screen)
  
  def reset(self):
    pass
  
  def keydown(self, event):
    pass
  
  def keyup(self, event):
    pass
  
  def mousemotion(self, event):
    if self.button.rect.collidepoint(event.pos):
      self.button.mousemotion(event)
  
  def mousedown(self, event):
    if self.button.rect.collidepoint(event.pos):
      self.button.mousedown(event)
  
  def mouseup(self, event):
    if self.button.rect.collidepoint(event.pos):
      self.button.mouseup(event)
    else:
      self.button.mousecancel()


current_screen = None
def create_optionscreen():
  global current_screen
  current_screen = OptionScreen(['option1', 'option2', 'option3', 'option4'], 'submit')
  current_screen.donehandler = switch_to_game

def switch_to_game(option):
  global current_screen,house_skin, bg_skin, catapult_skin
  #current_screen = GameScreen(house_skin, bg_skin, catapult_skin)
  current_screen = GameOverScreen(create_optionscreen)

create_optionscreen()

running = True

while running :
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      break
    elif event.type == MOUSEMOTION:
      current_screen.mousemotion(event)
    elif event.type == MOUSEBUTTONDOWN:
      current_screen.mousedown(event)
    elif event.type == MOUSEBUTTONUP:
      current_screen.mouseup(event)
    #elif event.type == KEY_DOWN:
    #  running = False
    #  break
  
  #camera.move((1, 0))
  
  screen.fill((0,0,0))
  #screen.blit(background, [-i for i in camera.getpos()])
  
  #allsprites.update(camera)
  #allsprites.draw(screen)
  
  current_screen.update()
  current_screen.draw(screen)
  pygame.display.flip()
  clock.tick(FPS)