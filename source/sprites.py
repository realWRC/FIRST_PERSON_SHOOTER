import pygame as pg
import os
from collections import deque
from source.settings import *


class Sprite:
    """
    The Sprite class is a base class for all sprites in the game. It defines
    the basic functionality required for rendering static objects on the
    screen relative to the player's position. This includes loading sprite
    images, calculating angles, distances, and positions for rendering in the
    game world.

    Attributes:
        game (Game): Reference to the main game instance.
        player (Player): Reference to the player instance.
        x, y (float): Sprite's position in the game world.
        image (Surface): Loaded sprite image.
        sx, sy (float): Relative position of the sprite to the player.
        thetaAngle (float): Angle between the sprite and the player.
        screenX (float): Horizontal screen position for rendering the sprite.
        distance (float): Distance between the player and the sprite.
        normDistance (float): Distance adjusted for the player's viewing angle.
        spriteHalfWidth (int): Half the width of the sprite when projected on
                               screen.
    """

    def __init__(
            self,
            game,
            position=(5, 4),
            scale=0.7,
            change=0.27,
            path='resources/sprites/static/plant.png'
    ):
        """
        Initializes the Sprite class with position, scaling, and image loading.
        Prepares the sprite for rendering in the game world.

        Args:
            game (Game): Reference to the game instance.
            position (tuple): Initial position of the sprite in the game world.
            scale (float): Scaling factor for the sprite.
            change (float): Vertical shift applied to the sprite.
            path (str): File path to the sprite image.
        """
        self.game = game
        self.player = game.player
        self.x, self.y = position
        self.image = pg.image.load(path).convert_alpha()
        self.IMG_WIDTH = self.image.get_width()
        self.IMG_HALF_WIDTH = self.image.get_width() // 2
        self.IMG_RATIO = self.IMG_WIDTH / self.image.get_height()
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = change
        self.sx, self.sy = 0, 0
        self.thetaAngle, self.screenX = 0, 0
        self.distance, self.normDistance = 1, 1
        self.spriteHalfWidth = 0

    def getSprite(self):
        """
        Calculates the relative position of the sprite to the player, the angle
        between the sprite and the player, and the distance for rendering. It
        ensures the sprite is within the player's field of view and prepares
        the sprite for projection.
        """
        px = self.x - self.player.x
        py = self.y - self.player.y
        self.sx, self.sy = px, py
        self.thetaAngle = math.atan2(py, px)
        deltaAngle = self.thetaAngle - self.player.angle
        if (px > 0 and self.player.angle > math.pi) or (px < 0 and py < 0):
            deltaAngle += math.tau

        deltaChange = deltaAngle / ANGLE_CHANGE
        self.screenX = (HALF_NUMB_RAYS + deltaChange) * SCALE
        self.distance = math.hypot(px, py)
        self.normDistance = self.distance * math.cos(deltaAngle)
        if -self.IMG_HALF_WIDTH < self.screenX < \
                (WIDTH + self.IMG_HALF_WIDTH) and self.normDistance > 0.5:
            self.getProjection()

    def getProjection(self):
        """
        Projects the sprite onto the screen based on its distance from the
        player. Calculates the projection size and position, then adds it
        to the game's render list.
        """
        projection = SCREEN_DISTANCE / self.normDistance * self.SPRITE_SCALE
        projectionWidth, projectionHeight = projection * self.IMG_RATIO, \
            projection
        image = pg.transform.scale(
                self.image, (projectionWidth, projectionHeight)
        )
        self.spriteHalfWidth = projectionWidth // 2
        heightDisplacment = projectionHeight * self.SPRITE_HEIGHT_SHIFT
        pos = self.screenX - self.spriteHalfWidth, HALF_HEIGHT - \
            projectionHeight // 2 + heightDisplacment

        # Append sprites to rendering list
        self.game.raycasting.objectRenderList.append(
                (self.normDistance, image, pos)
        )

    def update(self):
        """
        Updates the sprite's position and prepares it for rendering each frame
        by calling the `getSprite` method.
        """
        self.getSprite()


class AnimatedSprite(Sprite):
    """
    The AnimatedSprite class extends the base Sprite class and adds
    functionality for handling sprite animations. It loads multiple frames of
    animation and handles frame swapping based on time.

    Attributes:
        duration (int): Time interval between frame changes for the animation.
        path (str): Path to the folder containing animation frames.
        frames (deque): Queue of frames for the animation.
        durationPrev (int): Time of the last frame change, used to control
                            animation speed.
        animationTrigger (bool): Flag indicating whether to change frames.
    """

    def __init__(
            self,
            game,
            position=(5, 3.5),
            scale=0.7,
            change=0.27,
            duration=170,
            path='resources/sprites/animated/torch_one/0.png'
    ):
        """
        Initializes the AnimatedSprite class by loading frames for animation
        and setting the duration between frame changes.

        Args:
            game (Game): Reference to the game instance.
            position (tuple): Initial position of the animated sprite.
            scale (float): Scaling factor for the sprite.
            change (float): Vertical shift applied to the sprite.
            duration (int): Time interval between frame changes.
            path (str): File path to the first animation frame.
        """
        super().__init__(game, position, scale, change, path)
        self.duration = duration
        self.path = path.rsplit('/', 1)[0]
        self.frames = self.getFrames(self.path)
        self.durationPrev = pg.time.get_ticks()
        self.animationTrigger = False

    def getFrames(self, path):
        """
        Loads all frames for the animation from the specified folder path and
        returns them as a deque (double-ended queue).

        Args:
            path (str): The folder path containing the animation frames.

        Returns:
            deque: A deque containing the loaded frames for the animation.
        """
        frames = deque()
        for directory in os.listdir(path):
            if os.path.isfile(os.path.join(path, directory)):
                img = pg.image.load(path + '/' + directory).convert_alpha()
                frames.append(img)
        return frames

    def durationCheck(self):
        """
        Checks if enough time has passed since the last frame change. If so,
        it sets the animationTrigger flag to True, allowing the sprite to
        change frames.
        """
        self.animationTrigger = False
        currentTime = pg.time.get_ticks()
        if currentTime - self.durationPrev > self.duration:
            self.durationPrev = currentTime
            self.animationTrigger = True

    def animate(self, frames):
        """
        Rotates through the animation frames if the animationTrigger is set to
        True. Updates the sprite's image to the current frame.

        Args:
            frames (deque): A deque of animation frames.
        """
        if self.animationTrigger:
            frames.rotate(-1)
            self.image = frames[0]

    def update(self):
        """
        Updates the animated sprite by calling the base sprite update method,
        checking if it's time to change frames, and then updating the
        animation.
        """
        super().update()
        self.durationCheck()
        self.animate(self.frames)
