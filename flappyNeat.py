import pygame
import random
import os
import sys
import neat
import pickle
from src.Bird import Bird
from src.Pipe import Pipe
from src.Ground import Ground

IMAGE_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
HEIGHT = 800
WIDTH = 500

generation = 0

pygame.font.init()
POINTS_FONT = pygame.font.SysFont('arial', 40)


def draw_game(screen, birds, pipes, ground, points, use_ai=False, generation=0):
  screen.blit(IMAGE_BACKGROUND, (0,0))
  
  for bird in birds:
    bird.draw(screen)
  
  for pipe in pipes:
    pipe.draw(screen)
    
  ground.draw(screen)
  
  text = POINTS_FONT.render(f"Points: {points}", 0, (0,0,0))
  screen.blit(text, (WIDTH-10-text.get_width(),10))

  if use_ai:
    text = POINTS_FONT.render(f"Generation: {generation}", 0, (0,0,0))
    screen.blit(text, (10,10))
  
  pygame.display.update()

def main(genomes, config, use_ai=True):
  global generation
  generation += 1

  if use_ai:
    networks = []
    gen_list = []
    birds = []  
    for _, gen in genomes:
      network = neat.nn.FeedForwardNetwork.create(gen, config)
      networks.append(network)
      gen.fitness = 0
      gen_list.append(gen)
      birds.append(Bird(230,250))
  else:
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
      if not use_ai:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            for bird in birds: bird.fly()

    birds_colided = []
    curr_pipe_passed = False
    for n, bird in enumerate(birds):
      bird.move()
      if use_ai:
        gen_list[n].fitness += 0.2
        inputs = (
                  bird.y, 
                  abs(bird.y - pipes[-1].upper_pos),
                  abs(bird.y - pipes[-1].lower_pos)
                  )
        output = networks[n].activate(inputs)
        if output[0] > 0.5:
          bird.fly()
      for pipe in pipes:
        hit_pipe = pipe.colision(bird)
        hit_ground = ground.colision(bird)
        hit_ceiling = (bird.y < 0)
        if any([hit_pipe, hit_ground, hit_ceiling]):
          if n not in birds_colided: 
            birds_colided.append(n)
          if use_ai: 
            gen_list[n].fitness -= 5
        if (bird.x > pipe.x+pipe.lower_img.get_width() and pipe.passed == False):
          curr_pipe_passed = True
          pipe.passed = True
          if use_ai: 
            gen_list[n].fitness += 10

    ground.move()

    pipes_passed = []
    for n, pipe in enumerate(pipes):
      if (pipe.x + pipe.lower_img.get_width() < 0):
        pipes_passed.append(n)
      pipe.move()

    if curr_pipe_passed:
      points+=1
      pipes.append(Pipe(WIDTH+random.randint(50,150)))
      curr_pipe_passed = False
    
    for n in birds_colided[::-1]:
      birds.pop(n)
      if use_ai:
        networks.pop(n)
        gen_list.pop(n)

    for n in pipes_passed[::-1]:
      pipes.pop(n)

    if not birds:
      if use_ai:
        break
      pygame.quit()
      quit()

    draw_game(screen, birds, pipes, ground, points, use_ai, generation)

def saveGenome(winner, genome_file):
  with open(genome_file, "wb") as f:
    genome = pickle.dump(winner, f)

def loadGenome(genome_file):
  with open(genome_file, "rb") as f:
    genome = pickle.load(f)
  return genome
  
def run(config_file, use_ai, train):
  if use_ai:
    if train:
      config = neat.config.Config(neat.DefaultGenome,
                                  neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet,
                                  neat.DefaultStagnation,
                                  config_file)

      pop = neat.Population(config)
      pop.add_reporter(neat.StdOutReporter(True))
      pop.add_reporter(neat.StatisticsReporter())
      winner = pop.run(main, 50)
      saveGenome(winner, "winner.pkl")
    else:
      genome = loadGenome("winner.pkl")
      genomes = [(1, genome)]
      main(genomes, config, use_ai)
  else:
    main(None, None, use_ai)


if __name__ == "__main__":
  if len(sys.argv) == 1:
    inp = False
    train = False
  elif sys.argv[1] == "-h" or sys.argv[1] == "--help" or len(sys.argv) > 3:
    print("\n>>>--------->> Error! <<---------<<<")
    print("Usage: python3 flappyNeat.py [AI] [Train]")
    quit()
  else:
    inp = True if sys.argv[1].upper()=="AI" else False
    if len(sys.argv) == 3:
      train = True if sys.argv[2].upper()=="TRAIN" else False
    else:
      train = False
  run("config.dat", use_ai=inp, train=train)
 


