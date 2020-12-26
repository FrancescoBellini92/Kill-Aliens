import pygame, os, random

os.chdir( os.path.dirname(os.path.abspath(__file__)))


class Player(pygame.sprite.Sprite):

    def __init__(self,starting_pos):
        super().__init__()
        self.image=pygame.image.load("assets/images/player/player.png")
        self.explosions = [
            "assets/images/player/expl1.png",
            "assets/images/player/expl2.png",
            "assets/images/player/expl3.png",
            "assets/images/player/expl4.png"
        ]
        self.rect = self.image.get_rect(midbottom = starting_pos.midbottom)
        self.speed = [10, 0]
        self.reverse_speed = [-10, 0]
        self.stop = [0, 0]
        self.life = 0
        self.frame_duration = len(self.explosions) - 1 # 4 frames, as the pictures for explosion

    def update(self, speed, screen_rect):
        self.rect.x += speed[0]
        if self.rect.right > screen_rect.right or self.rect.left < screen_rect.left:
            self.rect.x -= speed[0]


    def death_sequence(self, scores, death_fn):
        self.image = pygame.image.load(self.explosions[self.life])
        self.life += 1
        if self.life == self.frame_duration:
            death_fn(scores)


class Alien(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("assets/images/alien/alien.png")
        self.rect = self.image.get_rect()
        self.pos = random.choice([ [0, 0], [800, 0] ])
        if self.pos == [0, 0]:
            self.speed = [10, 30]
        else:
            self.speed = [-10, 30]
            self.rect = self.image.get_rect(right = 800)


    def update(self, screen_rect):
        self.rect.x += self.speed[0]
        self.rect.y += 0
        if not screen_rect.contains(self.rect):
            self.speed[0] =- self.speed[0]
            self.rect.y += self.speed[1]
