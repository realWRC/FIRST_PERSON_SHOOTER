from source.sprites import *


class Weapon(AnimatedSprite):
    """Defines base class for all weapons"""

    def __init__(
            self,
            game,
            position=(11, 3.5),
            scale=1.5,
            duration=170,
            path='resources/sprites/weapons/shotgun/0.png'
    ):
        """Initialises Weapon class"""
        super().__init__(game, position, scale, change=0.27, duration=duration, path=path)
        self.frames = deque(
            [pg.transform.smoothscale(frame, (self.image.get_width() * scale, self.image.get_height() * scale))
             for frame in self.frames])
        self.weaponPosition = (HALF_WIDTH - self.frames[0].get_width() // 2, HEIGHT - self.frames[0].get_height())
    
    def draw(self):
        """Draws the Actual Weapon"""
        self.game.screen.blit(self.frames[0], self.weaponPosition)
    
    def update(self):
        pass
