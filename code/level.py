import pygame 
from support import import_csv_layout, import_cut_graphics
from tiles import Tile, StaticTile, Gems
from setting import *
from player import Player
from entity import Slime, Worm, Knight, Boss

from abc import ABC
from abc import abstractmethod


class LevelInitial(ABC):
        def __init__(self, level_data, surface, change_gems, change_health):
                self.display_surface = surface
                self.world_shift = 0
                self.current_level = 0
                self.boss_health = 0

                self.change_gems = change_gems
                self.win = False

        @abstractmethod
        def create_tile_group(self, layout, type):
                pass
        
        @abstractmethod
        def player_setup(self,layout,change_health):
                pass

class LevelFunction(ABC):
        def set_current_level(self, check_win):
                if check_win == True:
                        self.current_level += 1

        def horizontal_movement_collision(self):
                player = self.player.sprite
                player.collision_rect.x += player.direction.x * player.speed
                collidable_sprites = self.terrain_sprites.sprites()
                for sprite in collidable_sprites:
                        if sprite.rect.colliderect(player.collision_rect):
                                if player.direction.x < 0: 
                                        player.collision_rect.left = sprite.rect.right
                                        player.on_left = True
                                        self.current_x = player.rect.left
                                elif player.direction.x > 0:
                                        player.collision_rect.right = sprite.rect.left
                                        player.on_right = True
                                        self.current_x = player.rect.right

        def vertical_movement_collision(self):
                player = self.player.sprite
                player.apply_gravity()
                collidable_sprites = self.terrain_sprites.sprites()

                for sprite in collidable_sprites:
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

        
        def get_player_on_ground(self):
                if self.player.sprite.on_ground:
                        self.player_on_ground = True
                else:
                        self.player_on_ground = False

        def check_win(self):
                if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
                        self.win = True
                        return self.win
        
        def check_gems_collisions(self):
                collided_gems = pygame.sprite.spritecollide(self.player.sprite,self.gems_sprites,True)
                if collided_gems:
                        for gems in collided_gems:
                                pass
        
        def check_death(self):
                if self.player.sprite.health:
                        self.death = True
                        return self.death

        @abstractmethod        
        def check_enemy_collisions(self):
                pass

        @abstractmethod
        def run(self):
                pass

        @abstractmethod
        def check_fall(self):
                pass 


class LevelForest(LevelInitial, LevelFunction):
        def __init__(self, level_data, surface, change_gems, change_health):
                LevelInitial.__init__(self, level_data, surface, change_gems, change_health)

                # sprites setup
                player_layout = import_csv_layout(level_data['player'])
                self.player = pygame.sprite.GroupSingle()
                self.goal = pygame.sprite.GroupSingle()
                self.player_setup(player_layout, change_health)

                terrain_layout = import_csv_layout(level_data['terrain'])
                self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

                gems_layout = import_csv_layout(level_data['gems'])
                self.gems_sprites = self.create_tile_group(gems_layout,'gems')

                self.map = pygame.image.load('../level/images/level_0.png')

                constraint_layout = import_csv_layout(level_data['constraint'])
                self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')

                slime_layout = import_csv_layout(level_data['slime'])
                self.slime_sprites = self.create_tile_group(slime_layout,'slime')
                
        def create_tile_group(self, layout, type):
                sprite_group = pygame.sprite.Group()

                for row_index, row in enumerate(layout):
                        for col_index, value in enumerate(row):
                                if value != '-1':
                                        x = col_index * tile_size_0
                                        y = row_index * tile_size_0

                                        if type == 'terrain':
                                                terrain_tile_list = import_cut_graphics(tile_size_0, '../asset/terrain/forest/oak_woods_tileset.png')
                                                tile_surface = terrain_tile_list[int(value)]
                                                sprite = StaticTile(tile_size_0,x,y,tile_surface)
                                        if type == 'gems':
                                                sprite = Gems(16,x,y,'../asset/object')
                                        if type == 'slime':
                                                sprite = Slime(32, x, (y - 6), '../asset/enemy/slime/move')
                                        if type == 'constraint':
                                                sprite = Tile(tile_size_0, x, y)
                                        
                                        sprite_group.add(sprite)
		
                return sprite_group
        
        def player_setup(self,layout,change_health):
                for row_index, row in enumerate(layout):
                        for col_index,val in enumerate(row):
                                x = col_index * tile_size_0
                                y = row_index * tile_size_0
                                if val == '0':
                                        sprite = Player(x, y, self.display_surface, change_health, self.check_fall)
                                        self.player.add(sprite)
                                        self.spawn_x = x
                                        self.spawn_y = y
                                if val == '1':
                                        sprite = Tile(tile_size_0, x, y)
                                        self.goal.add(sprite)
        
        def check_enemy_collisions(self):
                enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.slime_sprites,False)
                if enemy_collisions:
                        for slime in enemy_collisions:
                                slime_center = slime.rect.centery
                                slime_top = slime.rect.top
                                player_bottom = self.player.sprite.rect.bottom
                                if slime_top < player_bottom < slime_center and self.player.sprite.direction.y >= 0:
                                        self.player.sprite.direction.y = -5
                                        slime.kill()
                                else:
                                        self.player.sprite.get_damage()

        def sprite_collision_reverse(self):
                for sprite in self.slime_sprites.sprites():
                        if pygame.sprite.spritecollide(sprite, self.constraint_sprites, False):
                                sprite.reverse()

        def check_fall(self):
                if self.player.sprite.rect.top > window_height:
                        self.fall = True
                        return self.fall

        def run(self):
                # update
                self.gems_sprites.update(self.world_shift)
                self.slime_sprites.update(self.world_shift)
                self.constraint_sprites.update(self.world_shift)
                self.player.update()
                self.goal.update(self.world_shift)

                # function
                self.sprite_collision_reverse()
                self.horizontal_movement_collision()
                self.get_player_on_ground()
                self.vertical_movement_collision()
                self.check_fall()
                self.check_win()
                self.check_gems_collisions()
                self.check_enemy_collisions()

                # draw on window
                self.goal.draw(self.display_surface)
                self.display_surface.blit(self.map, (0, 0))
                self.terrain_sprites.draw(self.display_surface)
                self.gems_sprites.draw(self.display_surface)
                self.slime_sprites.draw(self.display_surface)
                self.player.draw(self.display_surface)

class LevelCave(LevelInitial, LevelFunction):
        def __init__(self, level_data, surface, change_gems, change_health):
                LevelInitial.__init__(self, level_data, surface, change_gems, change_health)

                # sprites setup
                player_layout = import_csv_layout(level_data['player'])
                self.player = pygame.sprite.GroupSingle()
                self.goal = pygame.sprite.GroupSingle()
                self.player_setup(player_layout, change_health)

                terrain_layout = import_csv_layout(level_data['terrain'])
                self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

                gems_layout = import_csv_layout(level_data['gems'])
                self.gems_sprites = self.create_tile_group(gems_layout,'gems')

                self.map = pygame.image.load('../level/images/level_1.png')

                constraint_layout = import_csv_layout(level_data['constraint'])
                self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')

                worm_layout = import_csv_layout(level_data['worm'])
                self.worm_sprites = self.create_tile_group(worm_layout,'worm')
                
        def create_tile_group(self, layout, type):
                sprite_group = pygame.sprite.Group()

                for row_index, row in enumerate(layout):
                        for col_index, value in enumerate(row):
                                if value != '-1':
                                        x = col_index * tile_size_1
                                        y = row_index * tile_size_1

                                        if type == 'terrain':
                                                terrain_tile_list = import_cut_graphics(tile_size_1, '../asset/terrain/cave/mainlev_build.png')
                                                tile_surface = terrain_tile_list[int(value)]
                                                sprite = StaticTile(tile_size_1, x, y, tile_surface)
                                        if type == 'gems':
                                                sprite = Gems(16,x,y,'../asset/object')
                                        if type == 'worm':
                                                sprite = Worm(tile_size_1, x, y, '../asset/enemy/worm/move')
                                        if type == 'constraint':
                                                sprite = Tile(tile_size_1, x, y)
                                        
                                        sprite_group.add(sprite)
		
                return sprite_group
        
        def player_setup(self,layout,change_health):
                for row_index, row in enumerate(layout):
                        for col_index,val in enumerate(row):
                                x = col_index * tile_size_1
                                y = row_index * tile_size_1
                                if val == '0':
                                        sprite = Player(x, y, self.display_surface, change_health, self.check_fall)
                                        self.player.add(sprite)
                                        self.spawn_x = x
                                        self.spawn_y = y
                                if val == '1':
                                        sprite = Tile(tile_size_1, x, y)
                                        self.goal.add(sprite)

        def check_enemy_collisions(self):
                enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.worm_sprites,False)
                if enemy_collisions:
                        for worm in enemy_collisions:
                                worm_center = worm.rect.centery
                                worm_top = worm.rect.top
                                player_bottom = self.player.sprite.rect.bottom
                                if worm_top < player_bottom < worm_center and self.player.sprite.direction.y >= 0:
                                        self.player.sprite.direction.y = -5
                                        worm.kill()
                                else:
                                        self.player.sprite.get_damage()

        def sprite_collision_reverse(self):
                for sprite in self.worm_sprites.sprites():
                        if pygame.sprite.spritecollide(sprite, self.constraint_sprites, False):
                                sprite.reverse()

        def check_fall(self):
                if self.player.sprite.rect.top > window_height:
                        self.fall = True
                        return self.fall

        def run(self):
                # update
                self.gems_sprites.update(self.world_shift)
                self.worm_sprites.update(self.world_shift)
                self.constraint_sprites.update(self.world_shift)
                self.player.update()
                self.goal.update(self.world_shift)

                # function
                self.sprite_collision_reverse()
                self.horizontal_movement_collision()
                self.get_player_on_ground()
                self.vertical_movement_collision()
                self.check_fall()
                self.check_win()
                self.check_gems_collisions()
                self.check_enemy_collisions()
                
                # draw on window
                self.goal.draw(self.display_surface)
                self.display_surface.blit(self.map, (0, 0))
                self.terrain_sprites.draw(self.display_surface)
                self.gems_sprites.draw(self.display_surface)
                self.worm_sprites.draw(self.display_surface)
                self.player.draw(self.display_surface)

class LevelCastle(LevelInitial, LevelFunction):
        def __init__(self, level_data, surface, change_gems, change_health):
                LevelInitial.__init__(self, level_data, surface, change_gems, change_health)

                # sprites setup
                player_layout = import_csv_layout(level_data['player'])
                self.player = pygame.sprite.GroupSingle()
                self.goal = pygame.sprite.GroupSingle()
                self.player_setup(player_layout, change_health)

                terrain_layout = import_csv_layout(level_data['terrain'])
                self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

                gems_layout = import_csv_layout(level_data['gems'])
                self.gems_sprites = self.create_tile_group(gems_layout,'gems')

                self.map = pygame.image.load('../level/images/level_2.png')

                constraint_layout = import_csv_layout(level_data['constraint'])
                self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')

                knight_layout = import_csv_layout(level_data['knight'])
                self.knight_sprites = self.create_tile_group(knight_layout,'knight')
                
        def create_tile_group(self, layout, type):
                sprite_group = pygame.sprite.Group()

                for row_index, row in enumerate(layout):
                        for col_index, value in enumerate(row):
                                if value != '-1':
                                        x = col_index * tile_size_2
                                        y = row_index * tile_size_2

                                        if type == 'terrain':
                                                terrain_tile_list = import_cut_graphics(tile_size_2, '../asset/terrain/castle/main_lev_build.png')
                                                tile_surface = terrain_tile_list[int(value)]
                                                sprite = StaticTile(tile_size_2, x, y, tile_surface)
                                        if type == 'gems':
                                                sprite = Gems(16,x,y,'../asset/object')
                                        if type == 'knight':
                                                sprite = Knight(tile_size_2,x,y, '../asset/enemy/knight/idle', 20)
                                        if type == 'constraint':
                                                sprite = Tile(tile_size_2, x, y)
                                        
                                        sprite_group.add(sprite)
		
                return sprite_group
        
        def sprite_collision_reverse(self):
                for sprite in self.knight_sprites.sprites():
                        if pygame.sprite.spritecollide(sprite, self.constraint_sprites, False):
                                sprite.reverse()

        def player_setup(self,layout,change_health):
                for row_index, row in enumerate(layout):
                        for col_index,val in enumerate(row):
                                x = col_index * tile_size_2
                                y = row_index * tile_size_2
                                if val == '0':
                                        sprite = Player(x, y, self.display_surface, change_health, self.check_fall)
                                        self.player.add(sprite)
                                        self.spawn_x = x
                                        self.spawn_y = y
                                if val == '1':
                                        sprite = Tile(tile_size_2, x, y)
                                        self.goal.add(sprite)

        def check_enemy_collisions(self):
                enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.knight_sprites,False)
                if enemy_collisions:
                        for knight in enemy_collisions:
                                knight_center = knight.rect.centery
                                knight_top = knight.rect.top
                                player_bottom = self.player.sprite.rect.bottom
                                if knight_top < player_bottom < knight_center and self.player.sprite.direction.y >= 0:
                                        self.player.sprite.direction.y = -8
                                        knight.get_damage(10)
                                else:
                                        self.player.sprite.get_damage()

        def check_fall(self):
                if self.player.sprite.rect.top > window_height:
                        self.fall = True
                        return self.fall
                
        def respawn(self):
                if self.player.sprite.rect.top > window_height:
                        self.player.sprite.rect.x = self.spawn_x
                        self.player.sprite.rect.y = self.spawn_y

        def run(self):
                # update
                self.gems_sprites.update(self.world_shift)
                self.constraint_sprites.update(self.world_shift)
                self.knight_sprites.update(self.world_shift)
                self.player.update()
                self.goal.update(self.world_shift)

                # function
                self.sprite_collision_reverse()
                self.horizontal_movement_collision()
                self.get_player_on_ground()
                self.vertical_movement_collision()
                self.check_fall()
                self.check_win()
                self.check_gems_collisions()
                self.check_enemy_collisions()

                # draw on window
                self.goal.draw(self.display_surface)
                self.display_surface.blit(self.map, (0, 0))
                self.terrain_sprites.draw(self.display_surface)
                self.gems_sprites.draw(self.display_surface)
                self.knight_sprites.draw(self.display_surface)
                self.player.draw(self.display_surface)

class LevelCastleBoss(LevelInitial, LevelFunction):
        def __init__(self, level_data, surface, change_gems, change_health):
                LevelInitial.__init__(self, level_data, surface, change_gems, change_health)

                # sprites setup
                player_layout = import_csv_layout(level_data['player'])
                self.player = pygame.sprite.GroupSingle()
                self.goal = pygame.sprite.GroupSingle()
                self.player_setup(player_layout, change_health)

                terrain_layout = import_csv_layout(level_data['terrain'])
                self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

                self.map = pygame.image.load('../level/images/level_3.png')

                constraint_layout = import_csv_layout(level_data['constraint'])
                self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')

                boss_layout = import_csv_layout(level_data['boss'])
                self.boss_sprites = self.create_tile_group(boss_layout,'boss')
                
        def create_tile_group(self, layout, type):
                sprite_group = pygame.sprite.Group()

                for row_index, row in enumerate(layout):
                        for col_index, value in enumerate(row):
                                if value != '-1':
                                        x = col_index * tile_size_2
                                        y = row_index * tile_size_2

                                        if type == 'terrain':
                                                terrain_tile_list = import_cut_graphics(tile_size_2, '../asset/terrain/castle/main_lev_build.png')
                                                tile_surface = terrain_tile_list[int(value)]
                                                sprite = StaticTile(tile_size_2, x, y, tile_surface)
                                        if type == 'boss':
                                                sprite = Boss(tile_size_2,x,y, '../asset/enemy/boss/idle', 200, 0, 2)
                                        if type == 'constraint':
                                                sprite = Tile(tile_size_2, x, y)
                                        
                                        sprite_group.add(sprite)
		
                return sprite_group
        
        def sprite_collision_reverse(self):
                for sprite in self.boss_sprites.sprites():
                        if pygame.sprite.spritecollide(sprite, self.constraint_sprites, False):
                                sprite.reverse()

        def player_setup(self,layout,change_health):
                for row_index, row in enumerate(layout):
                        for col_index,val in enumerate(row):
                                x = col_index * tile_size_2
                                y = row_index * tile_size_2
                                if val == '0':
                                        sprite = Player(x, y, self.display_surface, change_health, self.check_fall)
                                        self.player.add(sprite)
                                        self.spawn_x = x
                                        self.spawn_y = y
                                if val == '1':
                                        sprite = Tile(tile_size_2, x, y)
                                        self.goal.add(sprite)

        def check_enemy_collisions(self):
                enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.boss_sprites,False)
                if enemy_collisions:
                        for boss in enemy_collisions:
                                boss_center = boss.rect.centery
                                boss_top = boss.rect.top
                                player_bottom = self.player.sprite.rect.bottom
                                self.boss_health = boss.health
                                if boss_top < player_bottom < boss_center and self.player.sprite.direction.y >= 0:
                                        self.player.sprite.direction.y = -18
                                        boss.get_damage(10)
                                else:
                                        self.player.sprite.get_damage()

        def check_win(self):
                if pygame.sprite.spritecollide(self.player.sprite, self.goal, False) and self.boss_health == 0:
                        self.win = True
                        return self.win

        def check_fall(self):
                if self.player.sprite.rect.top > window_height:
                        self.fall = True
                        return self.fall

        def run(self):
                # update
                self.constraint_sprites.update(self.world_shift)
                self.boss_sprites.update(self.world_shift)
                self.player.update()
                self.goal.update(self.world_shift)

                # function
                self.sprite_collision_reverse()
                self.horizontal_movement_collision()
                self.get_player_on_ground()
                self.vertical_movement_collision()
                self.check_fall()
                self.check_win()
                self.check_enemy_collisions()
                
                # draw on window
                self.goal.draw(self.display_surface)
                self.display_surface.blit(self.map, (0, 0))
                self.terrain_sprites.draw(self.display_surface)
                self.boss_sprites.draw(self.display_surface)
                self.player.draw(self.display_surface)