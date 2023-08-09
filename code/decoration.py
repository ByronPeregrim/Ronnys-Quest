from settings import vertical_tile_number, tile_size, screen_width, screen_height
import pygame
from tiles import AnimatedTile

class Background:
    def __init__(self):
        self.bg_images = []
        for i in range(1,6):
            bg_image = pygame.image.load(f'../graphics/decoration/background/{i}.png').convert_alpha()
            bg_image = pygame.transform.scale(bg_image,(screen_width,screen_height))
            self.bg_images.append(bg_image)
        self.bg_width = self.bg_images[0].get_width()

    
    def draw(self,surface,shift):
        for x in range(2):
            speed = 1
            for i in self.bg_images:
                surface.blit(i, ((x * self.bg_width) - shift * speed, 0))
                speed += 0.2

class Water:
    def __init__(self,top,level_width):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + screen_width) / water_tile_width) + 2
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192,x,y,'../graphics/decoration/water')
            self.water_sprites.add(sprite)

    def draw(self,surface,shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)