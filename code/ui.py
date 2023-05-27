import pygame


class UI:
    def __init__(self, surface):
        self.display_surface = surface

        # ui layer
        self.win_screen = pygame.image.load('../asset/ui/win.png')
        self.game_over_screen = pygame.image.load('../asset/ui/defeat.png')
        self.layout = pygame.image.load('../asset/ui/layout.png')
        self.controls = pygame.image.load('../asset/ui/controls.png')
        self.intro = pygame.image.load('../asset/ui/intro.png')
        self.start_menu = pygame.image.load('../asset/ui/start_up.png')

        # health
        self.bar = pygame.image.load('../asset/ui/bar.png').convert_alpha()
        self.bar_background = pygame.image.load('../asset/ui/bar_background.png').convert_alpha()
        self.current_health = pygame.image.load('../asset/ui/health_bar.png').convert_alpha()
        self.current_mana = pygame.image.load('../asset/ui/mana_bar.png').convert_alpha()
        self.bar_max_width = 200
        self.bar_height = 14

    def show_health(self, current, full):
        current_health_ratio = current / full
        current_bar_width = (self.bar_max_width * current_health_ratio) + 1
        if current > 0:
            self.current_health = pygame.transform.scale(self.current_health, (current_bar_width, 14))
            
            self.display_surface.blit(self.bar_background,(29,13))
            self.display_surface.blit(self.current_health,(29,13))
            self.display_surface.blit(self.bar,(20,11))
        else:
            self.display_surface.blit(self.bar_background,(29,13))
            self.display_surface.blit(self.bar,(20,11))

    def show_mana(self, current, full):
        current_mana_ratio = current / full
        current_bar_width = (self.bar_max_width * current_mana_ratio) + 1
        if current > 0:
            self.current_mana = pygame.transform.scale(self.current_mana, (current_bar_width, 14))
            
            self.display_surface.blit(self.bar_background,(29,50))
            self.display_surface.blit(self.current_mana,(29,50))
            self.display_surface.blit(self.bar,(20,48))
        else:
            self.display_surface.blit(self.bar_background,(29,50))
            self.display_surface.blit(self.bar,(20,48))

    def show_score(self, current_score):
        font = pygame.font.Font('../asset/ui/Minecraft.ttf', 12)
        score = font.render("SCORE " + str(current_score), True, 'white')
        self.display_surface.blit(score, (850, 11))

    def show_final_score(self, current_score):
        font = pygame.font.Font('../asset/ui/Minecraft.ttf', 20)
        score = font.render("SCORE " + str(current_score), True, 'black')
        score_rect = score.get_rect(center = (480, 530))
        self.display_surface.blit(score, score_rect)

    def show_stage(self, current_level):
        level_name = ["Forest Entrance", "Deep Forest", "Slime Lair", "Cave Entrance", "Deep Cave", "Worm Lair", "Castle Basement", "Broken Altar", "Throne Hall"]
        font = pygame.font.Font('../asset/ui/Minecraft.ttf', 16)
        if current_level >= 0 and current_level <= 8:
            current_level_name = font.render(level_name[current_level] , True, 'white')
            current_level_name_rect = current_level_name.get_rect(center = (850, 600))
            self.display_surface.blit(current_level_name, current_level_name_rect)