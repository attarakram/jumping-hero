import pygame


class UI:
    def __init__(self, surface):
        self.display_surface = surface

        # ui layer
        self.win_screen = pygame.image.load('../asset/ui/win.png')
        self.game_over_screen = pygame.image.load('../asset/ui/defeat.png')
        self.control_help = pygame.image.load('../asset/ui/control.png')
        self.start_menu = pygame.image.load('../asset/ui/start_up.png')

        # health
        self.health_bar = pygame.image.load('../asset/ui/bar.png').convert_alpha()
        self.health_bar_background = pygame.image.load('../asset/ui/bar_background.png').convert_alpha()
        self.current_health = pygame.image.load('../asset/ui/health_bar.png').convert_alpha()
        self.bar_max_width = 200
        self.bar_height = 14

    def show_health(self,current,full):
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        self.current_health = pygame.transform.scale(self.current_health, (current_bar_width, 14))
        
        self.display_surface.blit(self.health_bar_background,(29,12))
        self.display_surface.blit(self.current_health,(29,12))
        self.display_surface.blit(self.health_bar,(20,10))
