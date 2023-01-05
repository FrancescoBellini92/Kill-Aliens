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
        self.speed = [5, 0]
        self.reverse_speed = [-5, 0]
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
