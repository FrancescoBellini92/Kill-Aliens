import pygame, os

os.chdir( os.path.dirname(os.path.abspath(__file__)))


class EnemyShot(pygame.sprite.Sprite):
    """Shot fired by enemy ships"""

    def __init__(self, ship):
        super().__init__()
        self.image=pygame.image.load("assets/images/enemy/enemy_bomb.png")
        self.rect = self.image.get_rect(center = ship.rect.midbottom)
        self.speed = [0,3]
        return

    def update(self, screen_rect):
        self.rect.y += self.speed[1]

        if not screen_rect.contains(self.rect):
            self.kill()
