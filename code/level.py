import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Grass, Box, Bush, Tree, Coin
from enemy import Enemy
from decoration import Background, Water
from player import Player
from particles import ParticleEffect

class Level:
    def __init__(self,level_data,surface,change_coins):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.bg_shift = 0
        self.current_x = 0

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # user interface
        self.change_coins = change_coins

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')
        
        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout,'grass')

        # box setup
        box_layout = import_csv_layout(level_data['boxes'])
        self.box_sprites = self.create_tile_group(box_layout,'boxes')

        # bush setup
        bush_layout = import_csv_layout(level_data['bushes'])
        self.bush_sprites = self.create_tile_group(bush_layout,'bushes')

        # tree setup
        tree_layout = import_csv_layout(level_data['trees'])
        self.tree_sprites = self.create_tile_group(tree_layout,'trees')

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
        self.background = Background()
        self.level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 15,self.level_width)        

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrains/Tileset.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    
                    if type == 'grass':
                        sprite = Grass(tile_size,x,y,val)

                    if type == 'boxes':
                        sprite = Box(tile_size,x,y,val)

                    if type == 'bushes':
                        sprite = Bush(tile_size,x,y,val)

                    if type == 'trees':
                        sprite = Tree(tile_size,x,y,val)

                    if type == 'coins':
                        sprite = Coin(tile_size,x,y,'../graphics/coins/gold')

                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)

                    if type == 'constraints':
                        sprite = Tile(tile_size,x,y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '1': # Player
                    player_sprite = Player((x,y))
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
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_ = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right < self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

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

    def run(self):
        # run the entire level

        # decoration
        self.background.draw(self.display_surface,self.bg_shift)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # trees
        self.tree_sprites.update(self.world_shift)
        self.tree_sprites.draw(self.display_surface)

        # boxes
        self.box_sprites.update(self.world_shift)
        self.box_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        # bushes
        self.bush_sprites.update(self.world_shift)
        self.bush_sprites.draw(self.display_surface)
        
        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        # player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_coin_collisions()
        self.check_enemy_collisions()

        # water
        self.water.draw(self.display_surface,self.world_shift)

        # player
        self.scroll_x()
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        
