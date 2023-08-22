import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Grass, Box, Bush, Tree, Coin, Rock, Tube, Object, Power_Line, Chair, Checkpoint
from enemy import Enemy
from decoration import Background, Water
from player import Player
from particles import ParticleEffect
from game_data import levels
from ui import UI

class Level:
    def __init__(self,current_level,level_data,surface,create_overworld):
        # general setup
        self.display_surface = surface
        self.current_level = current_level
        level_data = levels[current_level]
        self.new_max_level = level_data['unlock']
        self.world_shift = 0
        self.bg_shift = 0
        self.current_x = 0
        self.create_overworld = create_overworld
        self.time = 0
        self.initial_time = pygame.time.get_ticks()
        self.ui = UI(surface)

        # level display
        self.font = pygame.font.Font(None,4)
        self.clock_font = pygame.font.Font('../graphics/ui/ARCADEPI.TTF',30)

        # game attributes
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.Group()
        self.player_setup(player_layout)

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')
        
        if self.current_level == 0 or self.current_level == 1:
            # grass setup
            grass_layout = import_csv_layout(level_data['grass'])
            self.grass_sprites = self.create_tile_group(grass_layout,'grass')

            # box setup
            box_layout = import_csv_layout(level_data['boxes'])
            self.box_sprites = self.create_tile_group(box_layout,'boxes')

            # tree setup
            tree_layout = import_csv_layout(level_data['trees'])
            self.tree_sprites = self.create_tile_group(tree_layout,'trees')

        if self.current_level == 2:
            tube_layout = import_csv_layout(level_data['tubes'])
            self.tube_sprites = self.create_tile_group(tube_layout,'tubes')

            object_layout = import_csv_layout(level_data['objects'])
            self.object_sprites = self.create_tile_group(object_layout,'objects')

            power_line_layout = import_csv_layout(level_data['power_lines'])
            self.power_line_sprites = self.create_tile_group(power_line_layout,'power_lines')

            chair_layout = import_csv_layout(level_data['chairs'])
            self.chair_sprites = self.create_tile_group(chair_layout,'chairs')

            background_tile_layout = import_csv_layout(level_data['background_tiles'])
            self.background_tile_sprites = self.create_tile_group(background_tile_layout,'background_tiles')

        # bush setup
        if self.current_level == 0:
            bush_layout = import_csv_layout(level_data['bushes'])
            self.bush_sprites = self.create_tile_group(bush_layout,'bushes')
        if self.current_level == 1:
            rock_layout = import_csv_layout(level_data['rocks'])
            self.rock_sprites = self.create_tile_group(rock_layout,'rocks')

        # coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coin_layout,'coins')

        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')

        # explosion particles
        self.explosion_sprites = pygame.sprite.Group()

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraints')

        # decoration 
        self.background = Background(self.current_level)
        self.level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 15,self.level_width,self.current_level)

        # checkpoint
        checkpoint_layout = import_csv_layout(level_data['checkpoint'])
        self.checkpoint_sprites = self.create_tile_group(checkpoint_layout,'checkpoint')

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        if self.current_level == 0:
                            terrain_tile_list = import_cut_graphics('../graphics/terrains/Tileset.png')
                        elif self.current_level == 1:
                            terrain_tile_list = import_cut_graphics('../graphics/terrains/Tileset1.png')
                        else:
                            terrain_tile_list = import_cut_graphics('../graphics/terrains/Tileset2.png')   
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    
                    if type == 'background_tiles':
                        background_tile_list = import_cut_graphics('../graphics/terrains/Tileset2.png')
                        tile_surface = background_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    
                    if type == 'grass':
                        sprite = Grass(tile_size,x,y,val,self.current_level)

                    if type == 'boxes':
                        sprite = Box(tile_size,x,y,val,self.current_level)

                    if type == 'bushes':
                        sprite = Bush(tile_size,x,y,val)

                    if type == 'rocks':
                        sprite = Rock(tile_size,x,y,val)

                    if type == 'tubes':
                        sprite = Tube(tile_size,x,y,val)
                    
                    if type == 'objects':
                        sprite = Object(tile_size,x,y,val)

                    if type == 'power_lines':
                        sprite = Power_Line(tile_size,x,y,val)

                    if type == 'chairs':
                        sprite = Chair(tile_size,x,y,val)

                    if type == 'trees':
                        sprite = Tree(tile_size,x,y,val,self.current_level)

                    if type == 'coins':
                        sprite = Coin(tile_size,x,y,'../graphics/coins/gold')

                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y,self.current_level)

                    if type == 'constraints':
                        sprite = Tile(tile_size,x,y)

                    if type == 'checkpoint':
                        sprite = Checkpoint(tile_size,x,y,'../graphics/player/checkpoint')

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '1': # Player
                    player_sprite = Player((x,y),self.change_health)
                    self.player.add(player_sprite)
                if val == '0': # Goal
                    goal_surface = pygame.image.load('../graphics/player/goal.png')
                    sprite = StaticTile(tile_size,x,y,goal_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()
                
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < (screen_width / 4) and direction_x < 0:
            self.world_shift = 5
            self.bg_shift -= 1
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -5
            self.bg_shift += 1
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coins_sprites,True)
        if collided_coins:
            for coin in collided_coins:
                self.change_coins(1)

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -11
                    explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level,0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False) and self.coins == 10:
            self.create_overworld(self.current_level,self.new_max_level)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_overworld(self.current_level,self.new_max_level)
        if keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level,0)

    def update_time(self):
            self.time = round(((pygame.time.get_ticks() - self.initial_time) / 1000),1)

    def show_clock(self,time):
        clock_amount_surf = self.clock_font.render(str(time) + '"',False,'gray')
        clock_amount_rect = clock_amount_surf.get_rect(topright = (1150,20))
        self.display_surface.blit(clock_amount_surf,clock_amount_rect)

    def change_coins(self,amount):
        self.coins += amount
    
    def change_health(self,amount):
        self.cur_health += amount

    def run(self):
        # run the entire level

        self.input()

        # decoration
        self.background.draw(self.display_surface,self.bg_shift)

        if self.current_level == 2:
            self.background_tile_sprites.update(self.world_shift)
            self.background_tile_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        if self.current_level == 0 or self.current_level == 1:
             # trees
            self.tree_sprites.update(self.world_shift)
            self.tree_sprites.draw(self.display_surface)

            # boxes
            self.box_sprites.update(self.world_shift)
            self.box_sprites.draw(self.display_surface)


        if self.current_level == 1:
            # rocks
            self.rock_sprites.update(self.world_shift)
            self.rock_sprites.draw(self.display_surface)

        if self.current_level == 2:
            # tubes
            self.tube_sprites.update(self.world_shift)
            self.tube_sprites.draw(self.display_surface)

            # objects
            self.object_sprites.update(self.world_shift)
            self.object_sprites.draw(self.display_surface)

            # power lines
            self.power_line_sprites.update(self.world_shift)
            self.power_line_sprites.draw(self.display_surface)

            # chairs
            self.chair_sprites.update(self.world_shift)
            self.chair_sprites.draw(self.display_surface)


        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        if self.current_level == 0:
            # bushes
            self.bush_sprites.update(self.world_shift)
            self.bush_sprites.draw(self.display_surface)
        
        if self.current_level == 0 or self.current_level == 1:
            # grass
            self.grass_sprites.update(self.world_shift)
            self.grass_sprites.draw(self.display_surface)

        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        # player sprites
        self.goal.update(self.world_shift)
        

        self.check_coin_collisions()
        self.check_enemy_collisions()

        self.check_death()
        self.check_win()

        # water
        self.water.draw(self.display_surface,self.world_shift)

        # player
        self.scroll_x()
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

        # checkpoint
        self.checkpoint_sprites.update(self.world_shift)
        self.checkpoint_sprites.draw(self.display_surface)

        # clock
        self.update_time()
        self.show_clock(self.time)

        # Health
        self.ui.show_health(self.cur_health,self.max_health)
        
        # Coins
        self.ui.show_coins(self.coins)
        
