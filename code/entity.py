import pygame 
from tiles import AnimatedTile
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

class Worm(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        self.rect.y += size - self.image.get_size()[1]
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

class Knight(AnimatedTile):
    def __init__(self, size, x, y, path, health):
        super().__init__(size, x, y, path)
        self.rect.y += size - self.image.get_size()[1]
        self.health = health
        self.speed = randint(0,1)

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
        else:
            self.kill()

    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()

class Boss(AnimatedTile):
    def __init__(self, size, x, y, path, health, speed1, speed2):
        super().__init__(size, x, y, path)
        self.rect.y += size - self.image.get_size()[1]
        self.health = health
        self.speed = randint(speed1, speed2)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1

    def change_speed(self):
        self.speed = randint(2, 4)

    def get_damage(self, damage):
        if self.health != 0:
            self.health -= 10
            self.change_speed()
        else:
            self.kill()

    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()