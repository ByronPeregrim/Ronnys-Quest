import pygame, sys
from settings import *
from level import Level
from game_data import level_0
from ui import UI
from overworld import Overworld

class Game:
    def __init__(self):
        self.max_level = 1
        self.overworld = Overworld(0,self.max_level,screen,self.create_level)
        self.status = 'overworld'
        
        # game attributes
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        # user interface
        self.ui = UI(screen)
        self.time = 0
    
    def change_coins(self,amount):
        self.coins += amount
    
    def change_health(self,amount):
        self.cur_health += amount
    
    def get_time(self):
        self.time = round((pygame.time.get_ticks() / 1000),1)

    def create_level(self,current_level):
        self.level = Level(current_level,level_0,screen,self.create_overworld,self.change_coins,self.change_health)
        self.status = 'level'
         
    def create_overworld(self,current_level,new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
        self.get_time()
        self.ui.show_health(self.cur_health,self.max_health)
        self.ui.show_coins(self.coins)
        self.ui.show_clock(self.time)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Ronny's Quest")
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    game.run()

    pygame.display.update()
    clock.tick(60)