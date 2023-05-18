import pygame
from pygame.locals import *
import sys
from setting import *
from level import *
from game_data import *
from ui import UI

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Jumping Hero")

class Game:
    def __init__(self):
        self.health = 100
        self.gems = 0

        self.game_level_0 = LevelForest(level_0, window, self.change_gems, self.change_health)
        self.game_level_1 = LevelCave(level_1, window, self.change_gems, self.change_health)
        self.game_level_2 = LevelCastle(level_2, window, self.change_gems, self.change_health)
        self.game_level_3 = LevelCastleBoss(level_3, window, self.change_gems, self.change_health)

        self.ui = UI(window)
        self.running = True
        self.restart = True
        self.current_level = -1

    def change_gems(self, amount, parameter):
        if parameter == True:
            self.gems += amount

    def change_health(self, amount):
        self.health += amount

    def check_game_over(self, parameter):
        if self.health <= 0 or parameter == True:
            self.current_level = 69

    def set_current_level(self, parameter):
        if parameter == True:
            if self.current_level == 69 or self.current_level == 4:
                self.current_level = -1
            else:
                self.current_level += 1

    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if self.current_level == 69 or self.current_level == 4:
            if keys[pygame.K_ESCAPE]:
                self.running = False
            if keys[pygame.K_r]:
                self.set_current_level(self.running)
        else:
            if keys[pygame.K_SPACE]:
                self.set_current_level(self.running)
    def run_0(self):
        self.game_level_0.run()
    
    def run_1(self):
        self.game_level_1.run()
    
    def run_2(self):
        self.game_level_2.run()
    
    def run_3(self):
        self.game_level_3.run()

game = Game()

while game.running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        
    window.fill((255,255,255))
        
    if game.current_level == -1:
        window.blit(game.ui.start_menu, (0,0))
        game.get_input()
    if game.current_level == 0:
        game.run_0()
        window.blit(game.ui.control_help,(0,0))
        game.ui.show_health(game.health, 1000)
        game.set_current_level(game.game_level_0.check_win())
        game.check_game_over(game.game_level_0.check_fall())
    if game.current_level == 1:
        game.run_1()
        window.blit(game.ui.control_help,(0,0))
        game.ui.show_health(game.health, 1000)
        game.set_current_level(game.game_level_1.check_win())
        game.check_game_over(game.game_level_0.check_fall())
    if game.current_level == 2:
        game.run_2()
        window.blit(game.ui.control_help,(0,0))
        game.ui.show_health(game.health, 1000)
        game.set_current_level(game.game_level_2.check_win())
        game.check_game_over(game.game_level_0.check_fall())
    if game.current_level == 3:
        game.run_3()
        window.blit(game.ui.control_help,(0,0))
        game.ui.show_health(game.health, 1000)
        game.set_current_level(game.game_level_3.check_win())
        game.check_game_over(game.game_level_0.check_fall())
    if game.current_level == 4:
        window.blit(game.ui.win_screen,(0, 0))
        game.get_input()
    if game.current_level == 69:
        window.fill('black')
        window.blit(game.ui.game_over_screen, (0, 0))
        game.get_input()

    pygame.display.update()
    FramePerSec.tick(FPS)
    
pygame.quit()
