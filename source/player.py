from source.settings import *
import pygame as pg
import math


class Player:
    """Defines the Player"""

    def __init__(self, game):
        """Initialises an instance of Player"""
        self.game = game
        self.x, self.y = PLAYER_POSITION
        self.angle = PLAYER_ANGLE

    def movement(self):
        """
        Controls movement of the player
            - speed is multiplies by deltaTime
              to keep the player speed independent
              of the frame rate
        """
        angleSin = math.sin(self.angle)
        angleCos = math.cos(self.angle)
        px, py = 0, 0
        speed = PLAYER_SPEED * self.game.deltaTime
        speedSin = speed * angleSin
        speedCos = speed * angleCos

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            px += speedCos
            py += speedSin
        if keys[pg.K_s]:
            px += -speedCos
            py += -speedSin
        if keys[pg.K_a]:
            px += speedSin
            py += -speedCos
        if keys[pg.K_d]:
            px += -speedSin
            py += speedCos

        self.wallCollision(px, py)

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROTATION_SPEED * self.game.deltaTime
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROTATION_SPEED * self.game.deltaTime

    def update(self):
        """Updates state of Player in core game loop"""
        self.movement()

    @property
    def position(self):
        """Returns Current Player Position"""
        return self.x, self.y

    @property
    def mapPosition(self):
        """Returns the tile on which the player is on"""
        return int(self.x), int(self.y)

    def getWallBounds(self, x, y):
        """Returns position if there is no wall"""
        if (x, y) not in self.game.map.gameWorld:
            return (x, y)

    def wallCollision(self, px, py):
        """Collision detection logic for player and walls"""
        if self.getWallBounds(int(self.x + px), int(self.y)):
            self.x += px
        if self.getWallBounds(int(self.x), int(self.y + py)):
            self.y += py

    def testDraw(self):
        """Created a 2d representation of the player on 2D map"""
        if LINEOFSIGHT is True:
            pg.draw.line(
                self.game.screen, "red", (self.x * 100, self.y * 100),
                (
                    self.x * 100 + WIDTH * math.cos(self.angle),
                    self.y * 100 + WIDTH * math.sin(self.angle)
                ),
                2
            )
        pg.draw.circle(
            self.game.screen,
            'green',
            (self.x * 100, self.y * 100),
            15
        )
