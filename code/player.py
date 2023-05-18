import pygame 
from support import import_folder
from math import sin
from setting import window_width, window_height

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, surface, change_health, check_fall):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.10
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = (x, y))
		self.spawn_x = x
		self.spawn_y = y

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 3
		self.gravity = 0.6
		self.jump_speed = -15
		self.collision_rect = pygame.Rect(self.rect.topleft, (30, 37))

		# player status
		self.status = 'idle'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False
		self.is_attacking = False
		self.check_fall = check_fall

		# health management
		self.change_health = change_health
		self.invincible = False
		self.invincibility_duration = 500
		self.hurt_time = 0

	def import_character_assets(self):
		character_path = '../asset/hero/'
		self.animations = {'idle':[], 'run':[], 'jump':[],'fall':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		if self.facing_right:
			self.image = image
			self.rect.bottomright = self.collision_rect.bottomright
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image
			self.rect.bottomleft = self.collision_rect.bottomleft

		if self.invincible:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT] and self.rect.x < window_width - 20:
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_LEFT] and self.rect.x > 0:
			self.direction.x = -1
			self.facing_right = False
		else:
			self.direction.x = 0

		if keys[pygame.K_SPACE] and self.on_ground:
			self.jump()
        
			
	def get_status(self):
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.collision_rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed

	def respawn(self):
		if self.check_fall == True:
			self.rect.x = self.spawn_x
			self.rect.y = self.spawn_y
			self.image.x = self.spawn_x
			self.image.y = self.spawn_y
			self.collision_rect = pygame.Rect(self.rect.topleft, (30, 37))
			self.get_damage()

	def get_damage(self):
		if not self.invincible:
			self.change_health(-5)
			self.invincible = True
			self.hurt_time = pygame.time.get_ticks()

	def invincibility_timer(self):
		if self.invincible:
			current_time = pygame.time.get_ticks()
			if current_time - self.hurt_time >= self.invincibility_duration:
				self.invincible = False

	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: return 255
		else: return 0

	def update(self):
		self.get_input()
		self.get_status()
		self.animate()
		self.invincibility_timer()
		self.wave_value()
		