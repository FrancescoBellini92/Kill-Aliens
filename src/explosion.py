import pygame, os

os.chdir( os.path.dirname(os.path.abspath(__file__)))


class Explosion(pygame.sprite.Sprite):
    """Explosion sprite of enemy bombs and collisions"""

    def __init__(self, obj):
        super().__init__()
        self.image = pygame.image.load("assets/images/misc/explosion.png")
        self.rect = self.image.get_rect(center = obj.rect.center)
        self.life = 3 # how many frames the object will be rendered

    def update(self):
        self.life -= 1
        if self.life < 1:
            self.kill()
