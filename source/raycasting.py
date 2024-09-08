import pygame as pg
import math
from source.settings import *


class RayCasting:
    """
    The RayCasting class defines the raycasting logic used to achieve a
    2.5D rendering effect. It simulates 3D perspectives in a 2D environment
    by casting rays from the player's position and calculating distances to
    the nearest walls, projecting them onto the screen.

    Attributes:
        game (Game): Reference to the main game instance.
        rayCastResult (list): Stores the results of each raycast, including
                              depth and texture information.
        objectRenderList (list): Stores the objects (walls) that need to be
                                 rendered on screen.
        textures (dict): A dictionary of wall textures used for rendering
                         walls.
    """

    def __init__(self, game):
        """
        Initializes the RayCasting class by linking it to the game instance
        and loading the wall textures for rendering.

        Args:
            game (Game): A reference to the main game object.
        """
        self.game = game
        self.rayCastResult = []
        self.objectRenderList = []
        self.textures = self.game.renderer.wallTextures

    def rayCast(self):
        """
        Implements the raycasting logic. For each ray, this method calculates
        the distance to the nearest vertical and horizontal walls, determines
        the wall texture, and adjusts for player movement and viewing angle.
        The result is used to render 2.5D visuals.
        """
        self.rayCastResult = []
        px, py = self.game.player.position
        mapX, mapY = self.game.player.mapPosition
        textureVert, textureHort = 1, 1

        rayAngle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUMB_RAYS):
            raySin = math.sin(rayAngle)
            rayCos = math.cos(rayAngle)

            # horizontals
            yHort, dy = (mapY + 1, 1) if raySin > 0 else (mapY - 1e-6, -1)
            depthHort = (yHort - py) / raySin
            xHort = px + depthHort * rayCos
            depthChange = dy / raySin
            dx = depthChange * rayCos

            for i in range(MAXIMUM_DEPTH):
                tileHort = int(xHort), int(yHort)
                if tileHort in self.game.map.gameWorld:
                    textureHort = self.game.map.gameWorld[tileHort]
                    break
                xHort += dx
                yHort += dy
                depthHort += depthChange

            # verticals
            xVert, dx = (mapX + 1, 1) if rayCos > 0 else (mapX - 1e-6, -1)
            depthVert = (xVert - px) / rayCos
            yVert = py + depthVert * raySin
            depthChange = dx / rayCos
            dy = depthChange * raySin

            for i in range(MAXIMUM_DEPTH):
                tileVert = int(xVert), int(yVert)
                if tileVert in self.game.map.gameWorld:
                    textureVert = self.game.map.gameWorld[tileVert]
                    break
                xVert += dx
                yVert += dy
                depthVert += depthChange

            # depth, texture offset
            if depthVert < depthHort:
                depth, texture = depthVert, textureVert
                yVert %= 1
                displacement = yVert if rayCos > 0 else (1 - yVert)
            else:
                depth, texture = depthHort, textureHort
                xHort %= 1
                displacement = (1 - xHort) if raySin > 0 else xHort

            if MODE == 'Test' and TESTMODE == '3D':
                depth *= math.cos(self.game.player.angle - rayAngle)
                projectionHeight = SCREEN_DISTANCE / (depth + 0.0001)
                color = [255 / (1 + depth ** 5 * 0.00001)] * 3
                pg.draw.rect(
                    self.game.screen,
                    color,
                    (
                        ray * SCALE, HALF_HEIGHT - projectionHeight // 2,
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
                projectionHeight = SCREEN_DISTANCE / (depth + 0.0001)
                self.rayCastResult.append(
                    (depth, projectionHeight, texture, displacement)
                )

            rayAngle += ANGLE_CHANGE

    def getObjectRenderList(self):
        """
        Prepares a list of objects (walls) to be rendered based on the results
        of the raycasting. This includes determining the size of the wall
        strips and their position on the screen based on distance from the
        player.
        """
        self.objectRenderList = []
        for ray, values in enumerate(self.rayCastResult):
            depth, projectionHeight, texture, displacement = values

            if projectionHeight < HEIGHT:
                wallStrip = self.textures[texture].subsurface(
                    displacement * (TEXTURE_SIZE - SCALE),
                    0,
                    SCALE, TEXTURE_SIZE
                )
                wallStrip = pg.transform.scale(
                        wallStrip, (SCALE, projectionHeight)
                )
                position = (ray * SCALE, HALF_HEIGHT - projectionHeight // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / projectionHeight
                wallStrip = self.textures[texture].subsurface(
                    displacement * (TEXTURE_SIZE - SCALE),
                    HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wallStrip = pg.transform.scale(wallStrip, (SCALE, HEIGHT))
                position = (ray * SCALE, 0)

            self.objectRenderList.append((depth, wallStrip, position))

    def update(self):
        """
        Updates the raycasting calculations by running the rayCast method to
        determine which walls are visible and how they should be rendered,
        followed by preparing the object render list for display.
        """
        self.rayCast()
        self.getObjectRenderList()
