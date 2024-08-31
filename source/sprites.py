import pygame as pg
import os
from collections import deque
from source.settings import *


class Sprite:
    """Base class for all Sprites"""

    def __init__(
            self,
            game,
            position=(10.5, 3.5),
            scale=0.7,
            change=0.27,
            path='resources/sprites/static/plant.png'
    ):
        """Initialises Sprite class"""
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
        """Gets sprote information relative to the player"""
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
        """Gets the position and distance values to be used for projection"""
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
        self.getSprite()


class AnimatedSprite(Sprite):
    """Defines methods for animated Sprites"""

    def __init__(
            self,
            game,
            position=(10.5, 4.5),
            scale=0.7,
            change=0.27,
            duration=170,
            path='resources/sprites/animated/torch_one/0.png'
    ):
        super().__init__(game, position, scale, change, path)
        self.duration = duration
        self.path = path.rsplit('/', 1)[0]
        self.frames = self.getFrames(self.path)
        self.durationPrev = pg.time.get_ticks()
        self.animationTrigger = False

    def getFrames(self, path):
        """Gets images/frames to use in the animation"""
        frames = deque()
        for directory in os.listdir(path):
            if os.path.isfile(os.path.join(path, directory)):
                img = pg.image.load(path + '/' + directory).convert_alpha()
                frames.append(img)
        return frames

    def durationCheck(self):
        """Determines weather to change frames via animation trigger"""
        self.animationTrigger = False
        currentTime = pg.time.get_ticks()
        if currentTime - self.durationPrev > self.duration:
            self.durationPrev = currentTime
            self.animationTrigger = True

    def animate(self, frames):
        """Swaps frames to render based on animationTrigger"""
        if self.animationTrigger:
            frames.rotate(-1)
            self.image = frames[0]

    def update(self):
        """Executes animation methods"""
        super().update()
        self.durationCheck()
        self.animate(self.frames)
