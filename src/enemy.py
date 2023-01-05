import pygame, os, random

os.chdir( os.path.dirname(os.path.abspath(__file__)))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_x, speed_y):
        super().__init__()
        self.image=pygame.image.load("assets/images/enemy/enemy.png")
        self.rect = self.image.get_rect()
        self.pos = random.choice([ [0, 0], [800, 0] ])
        if self.pos == [0, 0]:
            self.speed = [speed_x, speed_y]
        else:
            self.speed = [-5, 15]
            self.rect = self.image.get_rect(right = 800)


    def update(self, screen_rect):
        self.rect.x += self.speed[0]
        self.rect.y += 0
        if not screen_rect.contains(self.rect):
            self.speed[0] =- self.speed[0]
            self.rect.y += self.speed[1]
