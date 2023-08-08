from settings import vertical_tile_number, tile_size, screen_width, screen_height
import pygame

class Background:
    def __init__(self):
        self.bg_images = []
        for i in range(1,6):
            bg_image = pygame.image.load(f'../graphics/decoration/background/{i}.png').convert_alpha()
            bg_image = pygame.transform.scale(bg_image,(screen_width,screen_height))
            self.bg_images.append(bg_image)
        self.bg_width = self.bg_images[0].get_width()

    
    def draw(self,surface,shift):
        for x in range(5):
            speed = 1
            for i in self.bg_images:
                surface.blit(i, ((x * self.bg_width) - shift * speed, 0))
                speed += 0.2
