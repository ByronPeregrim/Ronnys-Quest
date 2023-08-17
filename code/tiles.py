import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self,shift):
        self.rect.x += shift

class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface 

class Grass(StaticTile):
    def __init__(self,size,x,y,val,current_level):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/{int(current_level)}/Grass/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Box(StaticTile):
    def __init__(self,size,x,y,val,current_level):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/{int(current_level)}/Boxes/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Bush(StaticTile):
    def __init__(self,size,x,y,val):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/0/Bushes/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Rock(StaticTile):
    def __init__(self,size,x,y,val):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/1/Rocks/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Tube(StaticTile):
    def __init__(self,size,x,y,val):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/2/tubes/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Object(StaticTile):
    def __init__(self,size,x,y,val):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/2/objects/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Power_Line(StaticTile):
    def __init__(self,size,x,y,val):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/2/power_lines/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Chair(StaticTile):
    def __init__(self,size,x,y,val):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/2/objects/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Tree(StaticTile):
    def __init__(self,size,x,y,val,current_level):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/{int(current_level)}/Trees/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class AnimatedTile(Tile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self,shift):
        self.animate()
        self.rect.x += shift

class Coin(AnimatedTile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y,path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x,center_y))