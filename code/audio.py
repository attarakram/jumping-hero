import pygame

pygame.init()

# channels
channel_ambience = pygame.mixer.Channel(0)
channel_soundtrack = pygame.mixer.Channel(1)
channel_enemies = pygame.mixer.Channel(2)
channel_sfx = pygame.mixer.Channel(3)
channel_player = pygame.mixer.Channel(4)
channel_spell = pygame.mixer.Channel(5)
channel_dying = pygame.mixer.Channel(6)

# ui
game_over = pygame.mixer.Sound('../audio/game_over_screen.ogg')
game_win = pygame.mixer.Sound('../audio/win_screen.ogg')
main_menu = pygame.mixer.Sound('../audio/main_menu.ogg')
intro = pygame.mixer.Sound('../audio/intro.ogg')

# ambience
soundtrack = pygame.mixer.Sound('../audio/soundtrack.ogg')
forest_ambience = pygame.mixer.Sound('../audio/forest_ambience.ogg')
cave_ambience = pygame.mixer.Sound('../audio/cave_ambience.wav')
castle_ambience = pygame.mixer.Sound('../audio/castle_ambience.ogg')

#player
jumping = pygame.mixer.Sound('../audio/jump.ogg')
hurt = pygame.mixer.Sound('../audio/hurt.ogg')
die = pygame.mixer.Sound('../audio/die.ogg')
heal = pygame.mixer.Sound('../audio/heal.ogg')
heartbeat = pygame.mixer.Sound('../audio/heartbeat.ogg')

# enemies = 
slime_die = pygame.mixer.Sound('../audio/slime_death.wav')
worm_die =pygame.mixer.Sound('../audio/worm_death.wav')
knight_hurt = pygame.mixer.Sound('../audio/knight_hurt.wav')
knight_die = pygame.mixer.Sound('../audio/knight_death.wav')

# sound fx
gems_pick = pygame.mixer.Sound('../audio/gems.wav')
level_win = pygame.mixer.Sound('../audio/win_level.wav')
