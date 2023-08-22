import pygame
from game_data import levels
from support import import_folder
from settings import screen_height,screen_width

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,status,icon_speed,path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center = pos)

        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2),self.rect.centery - (icon_speed / 2),icon_speed,icon_speed)

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (100,100))

    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            tint_surf = self.image.copy()
            tint_surf = pygame.image.load('../graphics/overworld/locked/1.png')
            tint_surf = pygame.transform.scale(tint_surf, (100,100))
            self.image = pygame.transform.scale(self.image, (100,100))
            self.image.blit(tint_surf,(0,0))
            
class Icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        self.frames = import_folder('../graphics/character/run')
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
    
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (50,50))

    def update(self):
        self.rect.center = self.pos
        self.animate()

class Overworld:
    def __init__(self,start_level,max_level,surface,create_level):

        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level
        self.big_font = pygame.font.Font('../graphics/ui/ARCADEPI.TTF',60)
        self.font = pygame.font.Font('../graphics/ui/ARCADEPI.TTF',30)

        # movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8

        # sprites
        self.setup_nodes()
        self.setup_icon()

        # time 
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 300

    def write_text(self):
        welcome_text_surf = self.big_font.render('Welcome to Ronny\'s Quest',False,'gray')
        welcome_text_rect = welcome_text_surf.get_rect(center = (screen_width / 2, screen_height / 15))
        self.display_surface.blit(welcome_text_surf,welcome_text_rect)

        instruction_text_surf_1 = self.font.render('To unlock the next level,',False,'gray')
        instruction_text_rect_1 = instruction_text_surf_1.get_rect(center = (screen_width / 2, screen_height - screen_height / 6))
        self.display_surface.blit(instruction_text_surf_1, instruction_text_rect_1)

        instruction_text_surf_2 = self.font.render('collect all coins and reach the checkpoint!',False,'gray')
        instruction_text_rect_2 = instruction_text_surf_2.get_rect(center = (screen_width / 2, screen_height - screen_height / 9))
        self.display_surface.blit(instruction_text_surf_2, instruction_text_rect_2)

        instruction_text_surf_3 = self.font.render('Press Space to start!',False,'gray')
        instruction_text_rect_3 = instruction_text_surf_3.get_rect(center = (screen_width / 2, screen_height - screen_height / 18))
        self.display_surface.blit(instruction_text_surf_3, instruction_text_rect_3)

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
    
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available',self.speed,node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], 'locked',self.speed,node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def draw_paths(self):
        points = [node['node_pos'] for index,node in enumerate(levels.values()) if index <= self.max_level]
        if self.max_level > 0:
            pygame.draw.lines(self.display_surface,'green',False,points,6)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self,target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)

        if target == 'next': 
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)


        return (end - start).normalize()

    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)

    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True

    def run(self):
        bg = pygame.image.load('../graphics/decoration/background/Background.png').convert_alpha()
        bg = pygame.transform.scale(bg,(screen_width,screen_height))
        self.display_surface.blit(bg,(0,0))
        self.input_timer()
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface) 
        self.icon.draw(self.display_surface)
        self.write_text()
