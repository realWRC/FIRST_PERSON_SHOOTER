from source.sprites import *


class Weapon(AnimatedSprite):
    """Defines base class for all weapons"""

    def __init__(
            self,
            game,
            position=(11, 3.5),
            scale=2,
            duration=55,
            path='resources/sprites/weapons/shotgun/0.png'
    ):
        """Initialises Weapon class"""
        super().__init__(
            game,
            position,
            scale,
            change=0.27,
            duration=duration,
            path=path
        )
        self.frames = deque(
            [pg.transform.smoothscale(frame, (
                self.image.get_width() * scale,
                self.image.get_height() * scale
                )
            )
             for frame in self.frames]
        )
        self.weaponPosition = (
            HALF_WIDTH - self.frames[0].get_width() // 2,
            HEIGHT - self.frames[0].get_height()
        )
        self.reload = False
        self.numFrames = len(self.frames)
        self.frameCounter = 0
        self.damage = 50

    def draw(self):
        """Draws the Actual Weapon"""
        self.game.screen.blit(self.frames[0], self.weaponPosition)

    def shoot(self):
        """Determines which frames should be used"""
        if self.reload:
            self.game.player.fire = False
            if self.animationTrigger:
                self.frames.rotate(-1)
                self.image = self.frames[0]
                self.frameCounter += 1
                if self.frameCounter == self.numFrames:
                    self.reload = False
                    self.frameCounter = 0

    def update(self):
        """Executes Weapom Methods"""
        self.durationCheck()
        self.shoot()
