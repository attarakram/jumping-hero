import pygame
from pygame.locals import *
import sys
from setting import *
from level import *
from game_data import *
from ui import UI
from score import Score
from audio import *
from map import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# making game window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Jumping Hero")

class Game:
    def __init__(self):
        # setting player health
        self.health = 100
        self.max_health = 100
        self.mana = 100
        self.max_mana = 100
        self.health_regen = self.max_health/1200
        self.mana_regen = 4

        # creating levels
        self.forest_0 = LevelForest(level_0, window, self.set_score, self.set_health, map_0)
        self.forest_1 = LevelForest(level_1, window, self.set_score, self.set_health, map_1)
        self.forest_2 = LevelForestBoss(level_2, window, self.set_score, self.set_health, map_2)

        self.cave_0 = LevelCave(level_3, window, self.set_score, self.set_health, map_3)
        self.cave_1 = LevelCave(level_4, window, self.set_score, self.set_health, map_4)
        self.cave_2 = LevelCaveBoss(level_5, window, self.set_score, self.set_health, map_5)

        self.castle_0 = LevelCastle(level_6, window, self.set_score, self.set_health, map_6)
        self.castle_1 = LevelCastle(level_7, window, self.set_score, self.set_health, map_7)
        self.castle_2 = LevelCastleBoss(level_8, window, self.set_score, self.set_health, map_8)

        # initialize ui, score, and other necessary variables
        self.ui = UI(window)
        self.score = Score()
        self.running = True
        self.restart = False
        self.checkpoint = 0
        self.current_level = -2

    def set_health(self, amount):
        self.health += amount

    def set_mana(self, amount):
        self.mana += amount

    def show_health_number(self):
        font = pygame.font.Font('../asset/ui/Minecraft.ttf', 8)
        hp = font.render(str(int(self.health)) + " / " + str(self.max_health), True, 'white')
        window.blit(hp, (50, 18))
    
    def show_mana_number(self):
        font = pygame.font.Font('../asset/ui/Minecraft.ttf', 8)
        mp = font.render(str(int(self.mana)) + " / " + str(self.max_mana), True, 'white')
        window.blit(mp, (50, 55))

    def max_health_multiplier(self, parameter):
        if parameter == True:
            self.max_health += 50

    def regen(self):
        if self.health < self.max_health and self.health >= 0:
            self.set_health(self.health_regen)
        elif self.health > self.max_health:
            self.health = self.max_health

        if self.mana < self.max_mana:
            self.set_mana(self.mana_regen)

    def set_score(self, amount):
            self.score.set_score(amount)

    def check_game_over(self, parameter):
        if self.health <= 0:
            channel_ambience.stop()
            channel_soundtrack.stop()
            self.current_level = 69
            die.play()
        elif parameter == True:
            channel_ambience.stop()
            channel_soundtrack.stop()
            self.health = 0
            self.current_level = 69
            die.play()

    def set_current_level(self, parameter):
        if parameter == True:
            if self.current_level == 69:
                self.current_level = self.checkpoint
                channel_soundtrack.play(soundtrack)
                channel_soundtrack.set_volume(0.5)
                if self.checkpoint == 0:
                    channel_ambience.play(forest_ambience)
                    channel_ambience.set_volume(0.2)
                elif self.checkpoint == 3:
                    channel_ambience.play(cave_ambience)
                    channel_ambience.set_volume(0.2)
                elif self.checkpoint == 6:
                    channel_ambience.play(castle_ambience)
                    channel_ambience.set_volume(0.2)
                self.set_score(-1000)
            elif self.current_level == 9:
                channel_soundtrack.play(soundtrack)
                channel_soundtrack.set_volume(0.5)
                if self.checkpoint == 0:
                    channel_ambience.play(forest_ambience)
                    channel_ambience.set_volume(0.2)
                elif self.checkpoint == 3:
                    channel_ambience.play(cave_ambience)
                    channel_ambience.set_volume(0.2)
                elif self.checkpoint == 6:
                    channel_ambience.play(castle_ambience)
                    channel_ambience.set_volume(0.2)
                self.current_level = 0
                self.set_score(self.score.get_score() * -1)
            else:
                self.current_level += 1

    def checkpoint_update(self):
        if self.current_level == 0 or self.current_level == 3 or self.current_level == 6:
            self.checkpoint = self.current_level
    
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if self.current_level == 69 or self.current_level == 9:
            if keys[pygame.K_ESCAPE]:
                self.running = False
            if keys[pygame.K_r]:
                self.restart = True
                game_over.stop()
                game_win.stop()

                self.forest_0 = LevelForest(level_0, window, self.set_score, self.set_health, map_0)
                self.forest_1 = LevelForest(level_1, window, self.set_score, self.set_health, map_1)
                self.forest_2 = LevelForestBoss(level_2, window, self.set_score, self.set_health, map_2)

                self.cave_0 = LevelCave(level_3, window, self.set_score, self.set_health, map_3)
                self.cave_1 = LevelCave(level_4, window, self.set_score, self.set_health, map_4)
                self.cave_2 = LevelCaveBoss(level_5, window, self.set_score, self.set_health, map_5)

                self.castle_0 = LevelCastle(level_6, window, self.set_score, self.set_health, map_6)
                self.castle_1 = LevelCastle(level_7, window, self.set_score, self.set_health, map_7)
                self.castle_2 = LevelCastleBoss(level_8, window, self.set_score, self.set_health, map_8)

                if self.current_level == 9:
                    self.max_health = 100
                self.health = self.max_health   
                self.score.reset_limit()

                self.set_current_level(self.restart)
        else:
            if keys[pygame.K_h]:
                if self.mana > 0 and self.health < self.max_health:
                    self.health_regen = (self.max_health/80)
                    self.mana_regen = 0
                    self.set_mana(-4)
                    channel_spell.queue(heal)
                else:
                    self.health_regen = (self.max_health/800)
            else:
                self.health_regen = (self.max_health/800)
                self.mana_regen = 4
                channel_spell.stop()

            if keys[pygame.K_TAB]:
                window.blit(self.ui.controls, (0,0))

    def run_0(self):
        self.forest_0.run()

    def run_1(self):
        self.forest_1.run()

    def run_2(self):
        self.forest_2.run()
    
    def run_3(self):
        self.cave_0.run()

    def run_4(self):
        self.cave_1.run()

    def run_5(self):
        self.cave_2.run()
    
    def run_6(self):
        self.castle_0.run()

    def run_7(self):
        self.castle_1.run()
    
    def run_8(self):
        self.castle_2.run()

game = Game()

while game.running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        if event.type == pygame.KEYDOWN:
            if game.current_level == -2 or game.current_level == -1:
                if event.key == pygame.K_SPACE:
                    game.set_current_level(game.running)
        
    window.fill((255,255,255))

    if game.current_level == -2:
        window.blit(game.ui.start_menu, (0,0))
        main_menu.set_volume(0.5)
        main_menu.play()
        channel_soundtrack.play(soundtrack)
        channel_soundtrack.set_volume(0.5)
    if game.current_level == -1:
        main_menu.stop()
        window.blit(game.ui.intro, (0,0))
        channel_ambience.play(forest_ambience)
        channel_ambience.set_volume(0.2)
    if game.current_level == 0:
        game.run_0()
        window.blit(game.ui.layout,(0,0))
        game.max_health_multiplier(game.score.multiplier_condition())
        game.ui.show_health(game.health, game.max_health)
        game.show_health_number()
        game.ui.show_mana(game.mana, game.max_mana)
        game.show_mana_number()
        game.regen()
        game.ui.show_score(game.score.get_score())
        game.set_current_level(game.forest_0.check_win())
        game.check_game_over(game.forest_0.check_fall())
        game.get_input()
        game.ui.show_stage(game.current_level)
        game.checkpoint_update()
    if game.current_level == 1:
        game.run_1()
        window.blit(game.ui.layout,(0,0))
        game.max_health_multiplier(game.score.multiplier_condition())
        game.ui.show_health(game.health, game.max_health)
        game.show_health_number()
        game.ui.show_mana(game.mana, game.max_mana)
        game.show_mana_number()
        game.regen()
        game.ui.show_score(game.score.get_score())
        game.set_current_level(game.forest_1.check_win())
        game.check_game_over(game.forest_1.check_fall())
        game.ui.show_stage(game.current_level)
        game.get_input()
    if game.current_level == 2:
        game.run_2()
        window.blit(game.ui.layout,(0,0))
        game.max_health_multiplier(game.score.multiplier_condition())
        game.ui.show_health(game.health, game.max_health)
        game.show_health_number()
        game.ui.show_mana(game.mana, game.max_mana)
        game.show_mana_number()
        game.regen()
        game.ui.show_score(game.score.get_score())
        game.set_current_level(game.forest_2.check_win())
        game.check_game_over(game.forest_2.check_fall())
        game.ui.show_stage(game.current_level)
        game.get_input()
        channel_ambience.play(cave_ambience)
        channel_ambience.set_volume(0.2)
    if game.current_level == 3:
        game.run_3()
        window.blit(game.ui.layout,(0,0))
        game.max_health_multiplier(game.score.multiplier_condition())
        game.ui.show_health(game.health, game.max_health)
        game.show_health_number()
        game.ui.show_mana(game.mana, game.max_mana)
        game.show_mana_number()
        game.regen()
        game.ui.show_score(game.score.get_score())
        game.set_current_level(game.cave_0.check_win())
        game.check_game_over(game.cave_0.check_fall())
        game.ui.show_stage(game.current_level)
        game.get_input()
        game.checkpoint_update()
    if game.current_level == 4:
        game.run_4()
        window.blit(game.ui.layout,(0,0))
        game.max_health_multiplier(game.score.multiplier_condition())
        game.ui.show_health(game.health, game.max_health)
        game.show_health_number()
        game.ui.show_mana(game.mana, game.max_mana)
        game.show_mana_number()
        game.regen()
        game.ui.show_score(game.score.get_score())
        game.set_current_level(game.cave_1.check_win())
        game.check_game_over(game.cave_1.check_fall())
        game.ui.show_stage(game.current_level)
        game.get_input()
    if game.current_level == 5:
        game.run_5()
        window.blit(game.ui.layout,(0,0))
        game.max_health_multiplier(game.score.multiplier_condition())
        game.ui.show_health(game.health, game.max_health)
        game.show_health_number()
        game.ui.show_mana(game.mana, game.max_mana)
        game.show_mana_number()
        game.regen()
        game.ui.show_score(game.score.get_score())
        game.set_current_level(game.cave_2.check_win())
        game.check_game_over(game.cave_2.check_fall())
        game.ui.show_stage(game.current_level)
        game.get_input()
        channel_ambience.play(castle_ambience)
        channel_ambience.set_volume(0.2)
    if game.current_level == 6:
        game.run_6()
        window.blit(game.ui.layout,(0,0))
        game.max_health_multiplier(game.score.multiplier_condition())
        game.ui.show_health(game.health, game.max_health)
        game.show_health_number()
        game.ui.show_mana(game.mana, game.max_mana)
        game.show_mana_number()
        game.regen()
        game.ui.show_score(game.score.get_score())
        game.set_current_level(game.castle_0.check_win())
        game.check_game_over(game.castle_0.check_fall())
        game.ui.show_stage(game.current_level)
        game.get_input()
        game.checkpoint_update()
    if game.current_level == 7:
        game.run_7()
        window.blit(game.ui.layout,(0,0))
        game.max_health_multiplier(game.score.multiplier_condition())
        game.ui.show_health(game.health, game.max_health)
        game.show_health_number()
        game.ui.show_mana(game.mana, game.max_mana)
        game.show_mana_number()
        game.regen()
        game.ui.show_score(game.score.get_score())
        game.set_current_level(game.castle_1.check_win())
        game.check_game_over(game.castle_1.check_fall())
        game.ui.show_stage(game.current_level)
        game.get_input()
    if game.current_level == 8:
        game.run_8()
        window.blit(game.ui.layout,(0,0))
        game.max_health_multiplier(game.score.multiplier_condition())
        game.ui.show_health(game.health, game.max_health)
        game.show_health_number()
        game.ui.show_mana(game.mana, game.max_mana)
        game.show_mana_number()
        game.regen()
        game.ui.show_score(game.score.get_score())
        game.set_current_level(game.castle_2.check_win())
        game.check_game_over(game.castle_2.check_fall())
        game.ui.show_stage(game.current_level)
        game.get_input()
    if game.current_level == 9:
        channel_ambience.stop()
        window.blit(game.ui.win_screen,(0, 0))
        game.ui.show_final_score(game.score.get_score())
        game.get_input()
    if game.current_level == 69:
        window.fill('black')
        game_over.play()
        game_over.set_volume(0.5)
        window.blit(game.ui.game_over_screen, (0, 0))
        game.get_input()

    pygame.display.update()
    FramePerSec.tick(FPS)
    
pygame.quit()