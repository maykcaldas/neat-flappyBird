import pygame
import random
import os
from src.Bird import Bird
from src.Pipe import Pipe
from src.Ground import Ground

IMAGE_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
HEIGHT = 800
WIDTH = 500

pygame.font.init()
POINTS_FONT = pygame.font.SysFont('arial', 40)


def draw_game(screen, birds, pipes, ground, points):
  screen.blit(IMAGE_BACKGROUND, (0,0))
  
  for bird in birds:
    bird.draw(screen)
  
  for pipe in pipes:
    pipe.draw(screen)
    
  ground.draw(screen)
  
  text = POINTS_FONT.render(f"Pontuação: {points}", 1, (0,0,0))
  screen.blit(text, (WIDTH-10-text.get_width(),10))
  
  pygame.display.update()

def main():

  birds = [Bird(230,250)]
  pipes = [Pipe(700)]
  ground = Ground(730)
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  points = 0
  clock = pygame.time.Clock()
  
  while True:
    clock.tick(30)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          for bird in birds: bird.fly()

    birds_colided = []
    curr_pipe_passed = False
    for n, bird in enumerate(birds):
      for pipe in pipes:
        hit_pipe = pipe.colision(bird)
        hit_ground = ground.colision(bird)
        hit_ceiling = (bird.y < 0)
        if any([hit_pipe, hit_ground, hit_ceiling]):
          birds_colided.append(n)
        if (bird.x > pipe.x and pipe.passed == False):
          curr_pipe_passed = True
          pipe.passed = True
      bird.move()
    ground.move()

    pipes_passed = []
    for n, pipe in enumerate(pipes):
      if (pipe.x + pipe.lower_img.get_width() < 0):
        pipes_passed.append(n)
      pipe.move()

    if curr_pipe_passed:
      points+=1
      pipes.append(Pipe(WIDTH+100))
      curr_pipe_passed = False
    
    for n in birds_colided[::-1]:
      birds.pop(n)

    for n in pipes_passed[::-1]:
      pipes.pop(n)

    print(pipes)

    if not birds:
      pygame.quit()
      quit()

    draw_game(screen, birds, pipes, ground, points)
  
  

if __name__ == "__main__":
  main()
  
  
  
  
  
  
