import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self,size,x,y,current_level):
        if current_level == 0:
            super().__init__(size,x,y,'../graphics/enemies/enemy/walk')
        elif current_level == 1:
            super().__init__(size,x,y,'../graphics/enemies/enemy/walk-1')
        else:
            super().__init__(size,x,y,'../graphics/enemies/enemy/walk-2')

        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(2,3)
        
        # Reduce enemy hitbox
        self.collision_rect = pygame.Rect(self.rect.midtop,(11,self.rect.height))
        self.rect = self.collision_rect
    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1
    
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()