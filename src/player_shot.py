import pygame, os

os.chdir( os.path.dirname(os.path.abspath(__file__)))

class PlayerShot(pygame.sprite.Sprite):
    """Shot fired by player"""

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/images/player/player_shot.png")
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = [0,-16]

    def update(self,screen_rect):
        self.rect.y += self.speed[1]

        if not screen_rect.contains(self.rect):
            self.kill
