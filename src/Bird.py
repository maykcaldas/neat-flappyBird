import pygame
import os

class Bird:
  MAX_ROTATION = 25
  VEL_ROTATION = 20
  TIME_ANIMATION = 5
  IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.angle = 0
    self.velocity = 0
    self.height = 0
    self.time = 0
    self.imageN = 1
    self.image = self.IMGS[1]
    
  def fly(self):
    self.velocity = -10.5
    self.time = 0
    self.height = self.y
    
  def move(self):
    # calcular o deslocamento
    self.time += 1
    deslocamento = 2.0 * (self.time**2) + self.velocity * self.time

    # restringir o deslocamento
    if deslocamento > 16:
        deslocamento = 16
    elif deslocamento < 0:
        deslocamento -= 2

    self.y += deslocamento

    # o angulo do passaro
    if deslocamento < 0:
        if self.angle < self.MAX_ROTATION:
            self.angle = self.MAX_ROTATION
    else:
        if self.angle > -75:
            self.angle -= self.VEL_ROTATION


  def draw(self, screen):
    self.imageN += 1
    
    if (self.imageN < self.TIME_ANIMATION):
      self.image = self.IMGS[0]
    elif self.imageN < self.TIME_ANIMATION*2:
      self.image = self.IMGS[1]
    elif self.imageN < self.TIME_ANIMATION*3:
      self.image = self.IMGS[2]
    elif self.imageN < self.TIME_ANIMATION*4:
      self.image = self.IMGS[1]
    elif self.imageN >= self.TIME_ANIMATION*4 + 1:
      self.image = self.IMGS[0]
      self.imageN = 0
      
    if self.angle < -50:
      self.image = self.IMGS[0]
      self.imageN = self.TIME_ANIMATION
    
    rotated_img = pygame.transform.rotate(self.image, self.angle)
    pos = self.image.get_rect(topleft=(self.x, self.y)).center
    rect = rotated_img.get_rect(center=pos)
    screen.blit(rotated_img, rect.topleft)
    
  def get_mask(self):
    return pygame.mask.from_surface(self.image)
    
    
    
    
