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

