# Global imports
import os, random 

# Pygame imports
import pygame
from pygame.locals import *
import pygame.font, pygame.event, pygame.draw, string

# Local imports
import graphics

###-------------------------------------------------------------------------###

# Constants
WIDTH = 800
HEIGHT = 600
AREA_SIZE = 1600, 600
FPS = 60

# Globals
current_screen = None
running = True

height_offset = 400
left_offset = 20

house_skin = 'default'
bg_skin = 'default'
catapult_skin = 'default'

## TODO: MOVE INTO FORMULAC CLASS ##
inequality = ' <= '
constants = [1, 2, 3, 4]
formula = 'x + y'
x,y,c=(0,0,0)

###-------------------------------------------------------------------------###

# Classes
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
    screen.blit(renderedText, 
               (self.rect.left + self.rect.width / 2. - renderedText.get_rect().width / 2., 
               self.rect.top + self.rect.height / 2. - renderedText.get_rect().height / 2.))
  
  def mousedown(self, event):
    self.mouseisdown = True
  
  def mouseup(self, event):
    self.mouseisdown = False
    self.onclick()
  
  def mousecancel(self):
    self.mouseisdown = False

  def mousemotion(self, event):
    pass
  

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
  
  def draw(self, screen):
    for button in self.buttons:
      button.draw(screen)

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

  def update(self):
    pass
      
  
  def reset(self):
    pass
  
  def keydown(self, event):
    pass
  
  def keyup(self, event):
    pass


class GameOverScreen(object):
  def __init__(self, retryclick):
    global WIDTH, HEIGHT
    self.button = Button(pygame.Rect(WIDTH / 2. - 100, HEIGHT - 200, 200, 100), 'Retry')
    self.button.onclick = retryclick
  
  def draw(self, screen):
    text = graphics.Graphics.renderText('\\s(26)Game Over')
    screen.blit(text, (screen.get_rect().width / 2. - text.get_rect().width / 2,
                       screen.get_rect().height / 2. - text.get_rect().height / 2))
    self.button.draw(screen)
  
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

  def update(self):
    pass
  
  def reset(self):
    pass
  
  def keydown(self, event):
    pass
  
  def keyup(self, event):
    pass

class formulac:
    """formula class"""
    def __init__(self, expression, inequality, optimal_val, difficulty=1):
        self.exp = expression
        self.ineq = inequality
        self.opt_v = optimal_val
        self.c = [self.opt_v]
        self.c.extend([random.normalvariate(self.opt_v,difficulty) in range(3)])

###-------------------------------------------------------------------------###

# Function Definitions 

## Helper functions ## 
def load_image(*path):
  image = pygame.image.load(os.path.join(os.getcwd(), 'data', *path)).convert()
  return image

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def choose_val(val, f_range=(0,1)):
  val_num = float('inf')
  while val_num < f_range[0] or val_num > f_range[1]:
    val_num = create_AskScreen("Give us "+val+": ")
    try:
        val_num = float(val_num)
    except ValueError: 
        pass
  return val_num


## Create_[X]Screen functions ##
def create_OptionScreen(options,done):
  global current_screen
  current_screen = OptionScreen(options, 'submit')
  current_screen.donehandler = done

def create_AskScreen(question):
  "ask(question) -> answer"
  pygame.font.init()
  current_string = ""
  display_box(question + current_string)
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    # check for
    #      negative      decimal               numbers
    elif inkey == 45 or inkey == 46 or (inkey >=48 and inkey <= 57):
      current_string += chr(inkey)
    display_box(question + current_string)
  return current_string

## Main functions ## 
def claim_chooser():
    optimal_val = 1
    options = [formula+inequality+str(c) for c in constants]
    create_OptionScreen(options,action_screen)

def action_screen(i):
    global c 
    c = constants[i]
    options = ["Strengthen claim", "Refute claim", "Agree with claim"]
    create_OptionScreen(options,switch_to_game)

def switch_to_game(option):
  global current_screen,house_skin, bg_skin, catapult_skin
  global x,y,c
  if option == 0:
      c = choose_val('c')
  elif option == 1:
     x = choose_val('x')
     y = choose_val('y')
  else:
    print eval(formula+inequality+str(c))
    current_screen = GameScreen(house_skin, bg_skin, catapult_skin)
  #current_screen = GameOverScreen(create_optionscreen)

###-------------------------------------------------------------------------###

# Run the program! 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

claim_chooser()

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
