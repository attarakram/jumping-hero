import pygame 
from support import import_csv_layout
from tiles import Tile, StaticTile, Gems
from setting import *
from player import Player
from entity import Slime, GiantSlime, Worm, GiantWorm, Knight, Boss
from audio import *

from abc import ABC
from abc import abstractmethod

class LevelInitial(ABC):
        def __init__(self, level_data, surface, set_score, set_health):
                # necessary variables initialization
                self.display_surface = surface
                self.world_shift = 0
                self.current_level = 0
                self.boss_health = 0

                # boolean variables initialization
                self.win = False
                self.gems_collide = False

        @abstractmethod
        def create_tile_group(self, layout, type):
                pass
        
        @abstractmethod
        def player_setup(self,layout,set_health):
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

        @abstractmethod
        def check_win(self):
                pass
        
        @abstractmethod
        def check_gems_collisions(self):
                pass

        @abstractmethod        
        def check_enemy_collisions(self):
                pass

        @abstractmethod
        def check_fall(self):
                pass 

        @abstractmethod
        def run(self):
                pass


class LevelForest(LevelInitial, LevelFunction):
        def __init__(self, level_data, surface, set_score, set_health, map):
                LevelInitial.__init__(self, level_data, surface, set_score, set_health)
                self.set_score = set_score

                # sprites setup
                player_layout = import_csv_layout(level_data['player'])
                self.player = pygame.sprite.GroupSingle()
                self.goal = pygame.sprite.GroupSingle()
                self.player_setup(player_layout, set_health)

                terrain_layout = import_csv_layout(level_data['terrain'])
                self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

                gems_layout = import_csv_layout(level_data['gems'])
                self.gems_sprites = self.create_tile_group(gems_layout,'gems')

                self.map = map

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
                                                sprite = Tile(tile_size_0, x, y)
                                        if type == 'gems':
                                                sprite = Gems(16,x,y,'../asset/object')
                                        if type == 'slime':
                                                sprite = Slime(32, x, (y - 6), '../asset/enemy/slime/move')
                                        if type == 'constraint':
                                                sprite = Tile(tile_size_0, x, y)
                                        
                                        sprite_group.add(sprite)
		
                return sprite_group
        
        def player_setup(self,layout,set_health):
                for row_index, row in enumerate(layout):
                        for col_index,val in enumerate(row):
                                x = col_index * tile_size_0
                                y = row_index * tile_size_0
                                if val == '0':
                                        sprite = Player(x, y, self.display_surface, set_health, self.check_fall,)
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
                                        channel_enemies.play(slime_die)
                                        self.set_score(50)
                                else:
                                        channel_player.queue(hurt)
                                        channel_player.set_volume(1.5)
                                        self.player.sprite.get_damage(-20)

        def sprite_collision_reverse(self):
                for sprite in self.slime_sprites.sprites():
                        if pygame.sprite.spritecollide(sprite, self.constraint_sprites, False):
                                sprite.reverse()
        
        def check_win(self):
                if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
                        channel_sfx.play(level_win)
                        self.win = True
                        return self.win
        
        def check_gems_collisions(self):
                collided_gems = pygame.sprite.spritecollide(self.player.sprite, self.gems_sprites, True)
                if collided_gems:
                        for gems in collided_gems:
                                channel_sfx.play(gems_pick)
                                self.set_score(50)

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
                self.terrain_sprites.draw(self.display_surface)
                self.display_surface.blit(self.map, (0, 0))
                self.gems_sprites.draw(self.display_surface)
                self.slime_sprites.draw(self.display_surface)
                self.player.draw(self.display_surface)

class LevelForestBoss(LevelInitial, LevelFunction):
        def __init__(self, level_data, surface, set_score, set_health, map):
                LevelInitial.__init__(self, level_data, surface, set_score, set_health)
                self.set_score = set_score
                self.boss_health = 150

                # sprites setup
                player_layout = import_csv_layout(level_data['player'])
                self.player = pygame.sprite.GroupSingle()
                self.goal = pygame.sprite.GroupSingle()
                self.player_setup(player_layout, set_health)

                terrain_layout = import_csv_layout(level_data['terrain'])
                self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

                gems_layout = import_csv_layout(level_data['gems'])
                self.gems_sprites = self.create_tile_group(gems_layout,'gems')

                self.map = map

                constraint_layout = import_csv_layout(level_data['constraint'])
                self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')

                boss_layout = import_csv_layout(level_data['boss'])
                self.boss_sprites = self.create_tile_group(boss_layout,'boss')

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
                                                sprite = Tile(tile_size_0, x, y)
                                        if type == 'gems':
                                                sprite = Gems(16,x,y,'../asset/object')
                                        if type == 'boss':
                                                sprite = GiantSlime(320, x, y, '../asset/enemy/giant_slime', 150)
                                        if type == 'slime':
                                                sprite = Slime(32, x, (y - 6), '../asset/enemy/slime/move')
                                        if type == 'constraint':
                                                sprite = Tile(tile_size_0, x, y)
                                        
                                        sprite_group.add(sprite)
		
                return sprite_group
        
        def player_setup(self,layout,set_health):
                for row_index, row in enumerate(layout):
                        for col_index,val in enumerate(row):
                                x = col_index * tile_size_0
                                y = row_index * tile_size_0
                                if val == '0':
                                        sprite = Player(x, y, self.display_surface, set_health, self.check_fall,)
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
                                        channel_enemies.play(slime_die)
                                        self.set_score(50)
                                else:
                                        channel_player.queue(hurt)
                                        channel_player.set_volume(1.5)
                                        self.player.sprite.get_damage(-20)

                enemy_collisions1 = pygame.sprite.spritecollide(self.player.sprite, self.boss_sprites,False)
                if enemy_collisions1:
                        for boss in enemy_collisions1:
                                boss_center = boss.rect.centery
                                boss_top = boss.rect.top
                                player_bottom = self.player.sprite.rect.bottom
                                self.boss_health = boss.health
                                if boss_top < player_bottom < boss_center and self.player.sprite.direction.y >= 0:
                                        self.player.sprite.direction.y = -20
                                        boss.get_damage()
                                        self.set_score(boss.reward)
                                elif self.player.sprite.collision_rect.y > boss_top:
                                        channel_player.queue(hurt)
                                        channel_player.set_volume(1.5)
                                        self.player.sprite.get_damage(-40)
                

        def sprite_collision_reverse(self):
                for sprite in self.boss_sprites.sprites():
                        if pygame.sprite.spritecollide(sprite, self.constraint_sprites, False):
                                sprite.reverse()

                for sprite in self.slime_sprites.sprites():
                        if pygame.sprite.spritecollide(sprite, self.constraint_sprites, False):
                                sprite.reverse()
        
        def check_win(self):
                if pygame.sprite.spritecollide(self.player.sprite, self.goal, False) and self.boss_health <= 0:
                        channel_sfx.play(level_win)
                        self.win = True
                        return self.win
        
        def check_gems_collisions(self):
                collided_gems = pygame.sprite.spritecollide(self.player.sprite, self.gems_sprites, True)
                if collided_gems:
                        for gems in collided_gems:
                                channel_sfx.play(gems_pick)
                                self.set_score(50)

        def check_fall(self):
                if self.player.sprite.rect.top > window_height:
                        self.fall = True
                        return self.fall

        def run(self):
                # update
                self.gems_sprites.update(self.world_shift)
                self.boss_sprites.update(self.world_shift)
                if self.boss_health == 0:
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
                self.terrain_sprites.draw(self.display_surface)
                self.display_surface.blit(self.map, (0, 0))
                if self.boss_health == 0:
                        self.slime_sprites.draw(self.display_surface)
                self.boss_sprites.draw(self.display_surface)
                self.gems_sprites.draw(self.display_surface)
                self.player.draw(self.display_surface)

class LevelCave(LevelInitial, LevelFunction):
        def __init__(self, level_data, surface, set_score, set_health, map):
                LevelInitial.__init__(self, level_data, surface, set_score, set_health)
                self.set_score = set_score

                # sprites setup
                player_layout = import_csv_layout(level_data['player'])
                self.player = pygame.sprite.GroupSingle()
                self.goal = pygame.sprite.GroupSingle()
                self.player_setup(player_layout, set_health)

                terrain_layout = import_csv_layout(level_data['terrain'])
                self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

                gems_layout = import_csv_layout(level_data['gems'])
                self.gems_sprites = self.create_tile_group(gems_layout,'gems')

                self.map = map

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
                                                sprite = Tile(tile_size_1, x, y)
                                        if type == 'gems':
                                                sprite = Gems(16,x,y,'../asset/object')
                                        if type == 'worm':
                                                sprite = Worm(58, x, y, '../asset/enemy/worm/move')
                                        if type == 'constraint':
                                                sprite = Tile(tile_size_1, x, y)
                                        
                                        sprite_group.add(sprite)
		
                return sprite_group
        
        def player_setup(self,layout,set_health):
                for row_index, row in enumerate(layout):
                        for col_index,val in enumerate(row):
                                x = col_index * tile_size_1
                                y = row_index * tile_size_1
                                if val == '0':
                                        sprite = Player(x, y, self.display_surface, set_health, self.check_fall)
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
                                        channel_enemies.play(worm_die)
                                        worm.kill()
                                        self.set_score(100)
                                else:
                                        channel_player.queue(hurt)
                                        channel_player.set_volume(1.5)
                                        self.player.sprite.get_damage(-30)

        def sprite_collision_reverse(self):
                for sprite in self.worm_sprites.sprites():
                        if pygame.sprite.spritecollide(sprite, self.constraint_sprites, False):
                                sprite.reverse()
        
        def check_win(self):
                if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
                        channel_sfx.play(level_win)
                        self.win = True
                        return self.win
        
        def check_gems_collisions(self):
                collided_gems = pygame.sprite.spritecollide(self.player.sprite, self.gems_sprites, True)
                if collided_gems:
                        for gems in collided_gems:
                                channel_sfx.play(gems_pick)
                                self.set_score(50)

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
                self.terrain_sprites.draw(self.display_surface)
                self.display_surface.blit(self.map, (0, 0))
                self.gems_sprites.draw(self.display_surface)
                self.worm_sprites.draw(self.display_surface)
                self.player.draw(self.display_surface)

class LevelCaveBoss(LevelInitial, LevelFunction):
        def __init__(self, level_data, surface, set_score, set_health, map):
                LevelInitial.__init__(self, level_data, surface, set_score, set_health)
                self.set_score = set_score
                self.boss_health = 150

                # sprites setup
                player_layout = import_csv_layout(level_data['player'])
                self.player = pygame.sprite.GroupSingle()
                self.goal = pygame.sprite.GroupSingle()
                self.player_setup(player_layout, set_health)

                terrain_layout = import_csv_layout(level_data['terrain'])
                self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

                gems_layout = import_csv_layout(level_data['gems'])
                self.gems_sprites = self.create_tile_group(gems_layout,'gems')

                self.map = map

                constraint_layout = import_csv_layout(level_data['constraint'])
                self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')

                worm_layout = import_csv_layout(level_data['worm'])
                self.worm_sprites = self.create_tile_group(worm_layout,'worm')

                boss_layout = import_csv_layout(level_data['boss'])
                self.boss_sprites = self.create_tile_group(boss_layout,'boss')
                
        def create_tile_group(self, layout, type):
                sprite_group = pygame.sprite.Group()

                for row_index, row in enumerate(layout):
                        for col_index, value in enumerate(row):
                                if value != '-1':
                                        x = col_index * tile_size_1
                                        y = row_index * tile_size_1

                                        if type == 'terrain':
                                                sprite = Tile(tile_size_1, x, y)
                                        if type == 'gems':
                                                sprite = Gems(16,x,y,'../asset/object')
                                        if type == 'worm':
                                                sprite = Worm(58, x, y, '../asset/enemy/worm/move')
                                        if type == 'boss':
                                                sprite = GiantWorm(174, x, y, '../asset/enemy/giant_worm', 150)
                                        if type == 'constraint':
                                                sprite = Tile(tile_size_1, x, y)
                                        
                                        sprite_group.add(sprite)
		
                return sprite_group
        
        def player_setup(self,layout,set_health):
                for row_index, row in enumerate(layout):
                        for col_index,val in enumerate(row):
                                x = col_index * tile_size_1
                                y = row_index * tile_size_1
                                if val == '0':
                                        sprite = Player(x, y, self.display_surface, set_health, self.check_fall,)
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
                                        channel_enemies.play(worm_die)
                                        worm.kill()
                                        self.set_score(100)
                                else:
                                        channel_player.queue(hurt)
                                        channel_player.set_volume(1.5)
                                        self.player.sprite.get_damage(-30)

                enemy_collisions_1 = pygame.sprite.spritecollide(self.player.sprite,self.boss_sprites,False)
                if enemy_collisions_1:
                        for boss in enemy_collisions_1:
                                boss_center = boss.rect.centery
                                boss_top = boss.rect.top -10
                                player_bottom = self.player.sprite.rect.bottom
                                self.boss_health = boss.health
                                if boss_top < player_bottom < boss_center and self.player.sprite.direction.y >= 0:
                                        self.player.sprite.direction.y = -14
                                        boss.get_damage()
                                        self.set_score(boss.reward)
                                elif self.player.sprite.collision_rect.y > boss_top:
                                        channel_player.queue(hurt)
                                        channel_player.set_volume(1.5)
                                        self.player.sprite.get_damage(-60)

        def sprite_collision_reverse(self):
                for sprite in self.worm_sprites.sprites():
                        if pygame.sprite.spritecollide(sprite, self.constraint_sprites, False):
                                sprite.reverse()

                for sprite in self.boss_sprites.sprites():
                        if pygame.sprite.spritecollide(sprite, self.constraint_sprites, False):
                                sprite.reverse()
        
        def check_win(self):
                if pygame.sprite.spritecollide(self.player.sprite, self.goal, False) and self.boss_health <= 0:
                        channel_sfx.play(level_win)
                        self.win = True
                        return self.win
        
        def check_gems_collisions(self):
                collided_gems = pygame.sprite.spritecollide(self.player.sprite, self.gems_sprites, True)
                if collided_gems:
                        for gems in collided_gems:
                                channel_sfx.play(gems_pick)
                                self.set_score(50)

        def check_fall(self):
                if self.player.sprite.rect.top > window_height:
                        self.fall = True
                        return self.fall

        def run(self):
                # update
                self.gems_sprites.update(self.world_shift)
                self.worm_sprites.update(self.world_shift)
                self.boss_sprites.update(self.world_shift)
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
                self.terrain_sprites.draw(self.display_surface)
                self.display_surface.blit(self.map, (0, 0))
                self.gems_sprites.draw(self.display_surface)
                self.worm_sprites.draw(self.display_surface)
                self.boss_sprites.draw(self.display_surface)
                self.player.draw(self.display_surface)

class LevelCastle(LevelInitial, LevelFunction):
        def __init__(self, level_data, surface, set_score, set_health, map):
                LevelInitial.__init__(self, level_data, surface, set_score, set_health)
                self.set_score = set_score

                # sprites setup
                player_layout = import_csv_layout(level_data['player'])
                self.player = pygame.sprite.GroupSingle()
                self.goal = pygame.sprite.GroupSingle()
                self.player_setup(player_layout, set_health)

                terrain_layout = import_csv_layout(level_data['terrain'])
                self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

                gems_layout = import_csv_layout(level_data['gems'])
                self.gems_sprites = self.create_tile_group(gems_layout,'gems')

                self.map = map

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
                                                sprite = Tile(tile_size_2, x, y)
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

        def player_setup(self,layout,set_health):
                for row_index, row in enumerate(layout):
                        for col_index,val in enumerate(row):
                                x = col_index * tile_size_2
                                y = row_index * tile_size_2
                                if val == '0':
                                        sprite = Player(x, y, self.display_surface, set_health, self.check_fall,)
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
                                        self.set_score(knight.reward)
                                elif self.player.sprite.collision_rect.y > knight_top:
                                        channel_player.queue(hurt)
                                        channel_player.set_volume(1.5)
                                        self.player.sprite.get_damage(-40)
        
        def check_win(self):
                if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
                        channel_sfx.play(level_win)
                        self.win = True
                        return self.win
        
        def check_gems_collisions(self):
                collided_gems = pygame.sprite.spritecollide(self.player.sprite, self.gems_sprites, True)
                if collided_gems:
                        for gems in collided_gems:
                                channel_sfx.play(gems_pick)
                                self.set_score(50)

        def check_fall(self):
                if self.player.sprite.rect.top > window_height:
                        self.fall = True
                        return self.fall

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
                self.terrain_sprites.draw(self.display_surface)
                self.display_surface.blit(self.map, (0, 0))
                self.gems_sprites.draw(self.display_surface)
                self.knight_sprites.draw(self.display_surface)
                self.player.draw(self.display_surface)

class LevelCastleBoss(LevelInitial, LevelFunction):
        def __init__(self, level_data, surface, set_score, set_health, map):
                LevelInitial.__init__(self, level_data, surface, set_score, set_health)
                self.set_score = set_score
                self.boss_health = 200

                # sprites setup
                player_layout = import_csv_layout(level_data['player'])
                self.player = pygame.sprite.GroupSingle()
                self.goal = pygame.sprite.GroupSingle()
                self.player_setup(player_layout, set_health)

                terrain_layout = import_csv_layout(level_data['terrain'])
                self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

                gems_layout = import_csv_layout(level_data['gems'])
                self.gems_sprites = self.create_tile_group(gems_layout,'gems')

                self.map = map

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
                                                sprite = Tile(tile_size_2, x, y)
                                        if type == 'gems':
                                                sprite = Gems(16,x,y,'../asset/object')
                                        if type == 'boss':
                                                sprite = Boss(98, x, y, '../asset/enemy/boss/idle', 200, 0, 2)
                                        if type == 'constraint':
                                                sprite = Tile(tile_size_2, x, y)
                                        
                                        sprite_group.add(sprite)
		
                return sprite_group
        
        def sprite_collision_reverse(self):
                for sprite in self.boss_sprites.sprites():
                        if pygame.sprite.spritecollide(sprite, self.constraint_sprites, False):
                                sprite.reverse()

        def player_setup(self,layout,set_health):
                for row_index, row in enumerate(layout):
                        for col_index,val in enumerate(row):
                                x = col_index * tile_size_2
                                y = row_index * tile_size_2
                                if val == '0':
                                        sprite = Player(x, y, self.display_surface, set_health, self.check_fall,)
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
                                boss_top = boss.rect.top -10
                                player_bottom = self.player.sprite.rect.bottom
                                self.boss_health = boss.health
                                if boss_top < player_bottom < boss_center and self.player.sprite.direction.y >= 0:
                                        self.player.sprite.direction.y = -18
                                        boss.get_damage()
                                        self.set_score(boss.reward)
                                else:
                                        channel_player.queue(hurt)
                                        channel_player.set_volume(1.5)
                                        self.player.sprite.get_damage(-80)
        
        def check_gems_collisions(self):
                collided_gems = pygame.sprite.spritecollide(self.player.sprite, self.gems_sprites, True)
                if collided_gems:
                        for gems in collided_gems:
                                channel_sfx.play(gems_pick)
                                self.set_score(50)

        def check_win(self):
                if pygame.sprite.spritecollide(self.player.sprite, self.goal, False) and self.boss_health == 0:
                        channel_sfx.play(level_win)
                        channel_soundtrack.play(game_win)
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
                self.terrain_sprites.draw(self.display_surface)
                self.display_surface.blit(self.map, (0, 0))
                self.boss_sprites.draw(self.display_surface)
                self.player.draw(self.display_surface)