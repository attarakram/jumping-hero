import pygame 
from tiles import AnimatedTile
from audio import *
from random import randint

class Slime(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(1,2)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1

    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()

class GiantSlime(AnimatedTile):
    def __init__(self, size, x, y, path, health):
        super().__init__(size, x, y, path)
        self.rect.y -= 148
        self.health = health
        self.speed = randint(0, 1)
        self.reward = 0

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1

    def change_speed(self):
        self.speed = randint(1, 2)

    def get_damage(self):
        if self.health >= 10:
            self.health -= 10
            self.change_speed()
            slime_die.set_volume(0.1)
            slime_die.play()
        else:
            slime_die.set_volume(0.2)
            slime_die.play()
            self.reward += 500
            self.kill()
    
    def score_reward(self):
        return self.reward

    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()

class Worm(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        self.rect.y -= 42
        self.speed = randint(2,3)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1

    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()

class GiantWorm(AnimatedTile):
    def __init__(self, size, x, y, path, health):
        super().__init__(size, x, y, path)
        self.rect.y -= 156
        self.health = health
        self.speed = randint(3, 4)
        self.reward = 0

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1

    def change_speed(self):
        self.speed = randint(4, 5)

    def get_damage(self):
        if self.health >= 10:
            self.health -= 10
            self.change_speed()
            worm_die.set_volume(0.1)
            worm_die.play()
        else:
            worm_die.set_volume(0.2)
            worm_die.play()
            self.reward += 500
            self.kill()
    
    def score_reward(self):
        return self.reward

    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()

class Knight(AnimatedTile):
    def __init__(self, size, x, y, path, health):
        super().__init__(size, x, y, path)
        self.rect.y += size - self.image.get_size()[1]
        self.health = health
        self.speed = randint(0,1)
        self.reward = 0

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1

    def get_damage(self, damage):
        if self.health != 0:
            self.health -= 10
            knight_hurt.set_volume(0.1)
            knight_hurt.play()
        else:
            knight_die.set_volume(0.1)
            knight_die.play()
            self.reward += 150
            self.kill()

    def score_reward(self):
        return self.reward

    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()

class Boss(AnimatedTile):
    def __init__(self, size, x, y, path, health, speed1, speed2):
        super().__init__(size, x, y, path)
        self.rect.y -= 66
        self.health = health
        self.speed = randint(speed1, speed2)
        self.reward = 0

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1

    def change_speed(self):
        self.speed = randint(2, 4)

    def get_damage(self):
        if self.health >= 10:
            self.health -= 10
            self.change_speed()
            knight_hurt.set_volume(0.1)
            knight_hurt.play()
        else:
            knight_die.set_volume(0.2)
            knight_die.play()
            self.reward += 500
            self.kill()
    
    def score_reward(self):
        return self.reward

    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()