import pygame
import os

class Ground:
  IMAGE_GROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
  WIDTH = IMAGE_GROUND.get_width()
  VELOCITY = 5
  
  def __init__(self, y):
    self.y = y
    self.x1 = 0
    self.x2 = self.WIDTH
    
  def move(self):
    self.x1 -= self.VELOCITY
    self.x2 -= self.VELOCITY
    
    if self.x1 + self.WIDTH < 0:
      self.x1 += 2*self.WIDTH
    if self.x2 + self.WIDTH < 0:
      self.x2 += 2*self.WIDTH    
      
  def draw(self, screen):
    screen.blit(self.IMAGE_GROUND, (self.x1, self.y) )
    screen.blit(self.IMAGE_GROUND, (self.x2, self.y) )
    
  def colision(self, bird):
    bird_mask = bird.get_mask()
    ground_mask =pygame.mask.from_surface(self.IMAGE_GROUND)

    ground_distance = (0, self.y - round(bird.y))

    ground_colision = bird_mask.overlap(ground_mask, ground_distance)
    
    return True if ground_colision else False
    
    
    
    
    
    
