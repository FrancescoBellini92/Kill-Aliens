import pygame, os

os.chdir( os.path.dirname(os.path.abspath(__file__)))


class EnemyExplosion(pygame.sprite.Sprite):
    """Explosion sprites of enemy ship"""

    def __init__(self, obj):
        super().__init__()
        self.images = [
            "assets/images/alien/alien_explod1.png",
            "assets/images/alien/alien_explod1.png",
            "assets/images/alien/alien_explod2.png",
            "assets/images/alien/alien_explod2.png",
            "assets/images/alien/alien_gone.png"
        ]
        self.image = pygame.image.load(self.images[0])
        self.rect = self.image.get_rect(center = obj.rect.center)
        self.life = 0
        self.frame_duration = len(self.images) - 1
        return

    def update(self):
        self.image = pygame.image.load(self.images[self.life])
        self.life += 1
        if self.life == self.frame_duration:
            self.kill()
        return

