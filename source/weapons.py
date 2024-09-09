from source.sprites import *


class Weapon(AnimatedSprite):
    """
    The Weapon class defines the base functionality for all weapons in the
    game. It extends the AnimatedSprite class and includes methods for
    shooting, reloading, and rendering the weapon on the screen.

    Attributes:
        frames (deque): A deque containing weapon animation frames, scaled
                        appropriately.
        weaponPosition (tuple): The position of the weapon on the screen.
        reload (bool): Flag indicating whether the weapon is in the process
                       of reloading.
        numFrames (int): The number of animation frames for the weapon.
        frameCounter (int): Keeps track of the current frame in the animation.
        damage (int): The damage dealt by the weapon when fired.
    """

    def __init__(
            self,
            game,
            position=(11, 3.5),
            scale=2,
            duration=50,
            path='resources/sprites/weapons/shotgun/0.png'
    ):
        """
        Initializes the Weapon class by loading and scaling the weapon's
        animation frames, setting the weapon's position on the screen, and
        preparing attributes for reloading and shooting logic.

        Args:
            game (Game): A reference to the main game object.
            position (tuple): The position of the weapon relative to the
                              player.
            scale (float): Scaling factor for the weapon's size.
            duration (int): The time between frame changes in the weapon
                            animation.
            path (str): File path to the weapon's sprite resources.
        """
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
        self.damage = 300

    def draw(self):
        """
        Renders the weapon on the screen at the specified position. This method
        is responsible for displaying the current frame of the weapon's
        animation.
        """
        self.game.screen.blit(self.frames[0], self.weaponPosition)

    def shoot(self):
        """
        Handles the shooting animation by rotating through the frames of the
        weapon animation. It checks if the weapon is reloading, and if so, it
        updates the frames accordingly and resets the reload status once the
        animation completes.
        """
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
        """
        Updates the weapon's state each frame. This method checks the duration
        between frames and triggers the shooting animation if the weapon is
        being fired.
        """
        self.durationCheck()
        self.shoot()
