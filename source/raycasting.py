import pygame as pg
import math
from source.settings import *


class RayCasting:
    """Defines the ray casting method to achieve 2.5 D"""

    def __init__(self, game):
        """Initialises teh RayCast class with the game instance"""
        self.game = game 

    def rayCast(self):
        """Defines raycasting logic"""
        px, py = self.game.player.position
        mapX, mapY = self.game.player.mapPosition

        rayAngle = self.game.player.angle - HFOV + 0.0001
        for ray in range(RAYS):
            raySin = math.sin(rayAngle)
            rayCos = math.cos(rayAngle)

            # Horizontal Intersections
            yHort, dy = (mapY + 1, 1) if raySin > 0 else (mapY - 1e-6, -1)
            depthHort = (yHort - py) / raySin
            xHort = px + depthHort * rayCos
            depthChange = dy / raySin
            dx = depthChange * rayCos

            for i in range(MAX_DEPTH):
                tileHort = int(xHort), int(yHort)
                if tileHort in self.game.map.gameWorld:
                    break
                xHort += dx
                yHort += dy
                depthHort += depthChange

            # Vertical Instersections
            xVert, dx = (mapX + 1, 1) if rayCos > 0 else (mapX - 1e-6, -1)
            depthVert = (xVert - px) / rayCos
            yVert = py + depthVert * raySin
            depthChange = dx / rayCos
            dy = depthChange * raySin

            for i in range(MAX_DEPTH):
                tileVert = int(xVert), int(yVert)
                if tileVert in self.game.map.gameWorld:
                    break
                xVert += dx
                yVert += dy
                depthVert += depthChange

            if depthHort < depthVert:
                depth = depthHort
            else:
                depth = depthVert
            depth *= math.cos(self.game.player.angle - rayAngle)

            # When True Renders In 3d, else 2D for testing
            if MODE is True:
                projectionHeight = SCREENDISTANCE / (depth + 0.0001)
                color = [255 / (1 + depth ** 5 * 0.00001)] * 3
                pg.draw.rect(
                    self.game.screen,
                    color,
                    (
                        ray * SCALE, HALFHEIGHT - projectionHeight // 2,
                        SCALE, projectionHeight
                    )
                )
            else:
                pg.draw.line(
                        self.game.screen, 'yellow', (100 * px, 100 * py),
                        (
                            100 * px + 100 * depth * rayCos,
                            100 * py + 100 * depth * raySin
                        ),
                        2
                )
            rayAngle += ANGLECHANGE

    def update(self):
        """Updates the RayCast state"""
        self.rayCast()
