import pygame
import os
import random

class Pipe:
  IMAGE_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
  DISTANCE = random.randint(150,250)
  VELOCITYX = random.randint(3,8)
  VELOCITYY = 5
  
  def __init__(self, x):
    self.x = x
    self.height = 0
    self.y_max = 500
    self.y_min = 200
    self.lower_img = self.IMAGE_PIPE
    self.lower_pos = 0
    self.upper_img = pygame.transform.flip(self.IMAGE_PIPE, False, True)
    self.upper_pos = 0
    self.passed = False
    self.get_height()
    self.rising = True if random.randint(0,10)>4 else False
    
  def get_height(self):
    self.height = random.randrange(self.y_min, self.y_max)

  def get_pos(self):
    self.lower_pos = self.height + self.DISTANCE/2
    self.upper_pos = self.height - self.DISTANCE/2 - self.upper_img.get_height()
    
  def move(self):
    self.x -= self.VELOCITYX
    if self.height >= self.y_max:
      self.rising = False
    if self.height <= self.y_min:
      self.rising = True
    self.height += self.VELOCITYY if self.rising else -self.VELOCITYY
    
  
  def draw(self, screen):
    self.get_pos()
    screen.blit(self.lower_img, (self.x, self.lower_pos) )
    screen.blit(self.upper_img, (self.x, self.upper_pos) )

  def colision(self, bird):
    bird_mask = bird.get_mask()
    upper_mask = pygame.mask.from_surface(self.upper_img)
    lower_mask =pygame.mask.from_surface(self.lower_img)
    
    upper_distance = (self.x - bird.x, self.upper_pos - round(bird.y))
    lower_distance = (self.x - bird.x, self.lower_pos - round(bird.y))
    
    upper_colision = bird_mask.overlap(upper_mask, upper_distance)
    lower_colision = bird_mask.overlap(lower_mask, lower_distance)
    
    return True if (upper_colision or lower_colision) else False
    
    
    
    
    
