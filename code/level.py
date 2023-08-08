import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size
from tiles import Tile, StaticTile, Grass, Box, Bush, Tree, Coin
from enemy import Enemy
from decoration import Background

class Level:
    def __init__(self,level_data,surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.bg_shift = 0

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

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

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraints')

        # decoration 
        self.background = Background()

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
                    print('player goes here')
                if val == '0': # Goal
                    goal_surface = pygame.image.load('../graphics/player/goal.png')
                    sprite = StaticTile(tile_size,x,y,goal_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()

    def run(self):
        # run the entire level
        self.world_shift = 0
        
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.bg_shift > 0:
            self.bg_shift -= 5
            self.world_shift = 5
        if key[pygame.K_RIGHT] and self.bg_shift < 2640:
            self.bg_shift += 5
            self.world_shift = -5

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