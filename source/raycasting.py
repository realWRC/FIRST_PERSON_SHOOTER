import pygame as pg
import math
from source.settings import *


class RayCasting:
    """Defines the ray casting method to achieve 2.5 D"""

    def __init__(self, game):
        """Initialises teh RayCast class with the game instance"""
        self.game = game
        self.rayCastResult = []
        self.objectRenderList = []
        self.textures = self.game.renderer.wallTexture

    def getObjectRenderList(self):
        """Get object render list"""
        self.objectRenderList = []
        for ray, values in enumerate(self.rayCastResult):
            depth, projectionHeight, texture, displacement = values

            if projectionHeight < HEIGHT:
                wallStrip = self.textures[texture].subsurface(
                    displacement * (TEXTURESIZE - SCALE), 0, SCALE, TEXTURESIZE
                )
                wallStrip = pg.transform.scale(
                    wallStrip, (SCALE, projectionHeight)
                )
                position = (ray * SCALE, HALFHEIGHT - projectionHeight // 2)
            else:
                textureHeight = TEXTURESIZE * HEIGHT / projectionHeight
                wallStrip = self.textures[texture].subsurface(
                    displacement * (TEXTURESIZE - SCALE),
                    HALFTEXTURESIZE - (textureHeight // 2),
                    SCALE,
                    textureHeight
                )
                wallStrip = pg.transform.scale(
                    wallStrip, (SCALE, HEIGHT)
                )
                position = (ray * SCALE, 0)

            self.objectRenderList.append((depth, wallStrip, position))

    def rayCast(self):
        """Defines raycasting logic"""
        self.rayCastResult = []
        px, py = self.game.player.position
        mapX, mapY = self.game.player.mapPosition
        textureVert, textureHort = 1, 1

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
                    textureHort = self.game.map.gameWorld[tileHort]
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
                    textureVert = self.game.map.gameWorld[tileVert]
                    break
                xVert += dx
                yVert += dy
                depthVert += depthChange

            if depthHort < depthVert:
                depth, texture = depthHort, textureHort
                xHort %= 1
                displacement = (1 - xHort) if raySin > 0 else xHort
            else:
                depth, texture = depthVert, textureVert
                yVert %= 1
                displacement = yVert if rayCos > 0 else (1 - yVert)

            # Testing Logic
            if MODE == 'Test' and TESTMODE == '3D':
                depth *= math.cos(self.game.player.angle - rayAngle)
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
            elif MODE == 'Test' and TESTMODE == '2D':
                pg.draw.line(
                        self.game.screen, 'yellow', (100 * px, 100 * py),
                        (
                            100 * px + 100 * depth * rayCos,
                            100 * py + 100 * depth * raySin
                        ),
                        2
                )
            else:
                depth *= math.cos(self.game.player.angle - rayAngle)
                projectionHeight = SCREENDISTANCE / (depth + 0.0001)
                self.rayCastResult.append(
                    (depth, projectionHeight, texture, displacement)
                )

            rayAngle += ANGLECHANGE

    def update(self):
        """Updates the RayCast state"""
        self.rayCast()
        self.getObjectRenderList()
