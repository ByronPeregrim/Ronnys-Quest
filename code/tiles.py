import pygame

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
    def __init__(self,size,x,y,val):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/Grass/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Box(StaticTile):
    def __init__(self,size,x,y,val):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/Boxes/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Bush(StaticTile):
    def __init__(self,size,x,y,val):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/Bushes/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Tree(StaticTile):
    def __init__(self,size,x,y,val):
        super().__init__(size,x,y,pygame.image.load(f'../graphics/decoration/Trees/{int(val)+1}.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))
