import pygame, sys
from settings import *
from level import Level
from game_data import level_0
from ui import UI

class Game:
    def __init__(self):
        
        # game attributes
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        # user interface
        self.ui = UI(screen)
        
    
    def run(self):
        self.ui.show_health(self.cur_health,self.max_health)
        self.ui.show_coins(self.coins)



# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Ronny's Quest")
clock = pygame.time.Clock()
level = Level(level_0,screen)
game = Game()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    level.run()
    game.run()

    pygame.display.update()
    clock.tick(60)