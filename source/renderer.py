import pygame as pg
from source.settings import *


class Renderer:
    def __init__(self, game):
        """Defines methods for rendering objects"""
        self.game = game
        self.screen = game.screen
        self.wallTextures = self.loadWallTextures()
        self.skyDisplacement = 0
        self.skyTexture = self.getTexture(
                'resources/textures/stars.png',
                (WIDTH, HALF_HEIGHT)
        )
        self.gameOver = self.getTexture(
            'resources/textures/game_over.png',
            RES,
        )
        self.gameFont = pg.font.Font('resources/fonts/Pixeltype.ttf', 50)
        self.gameOptionsFont = pg.font.Font('resources/fonts/Pixeltype.ttf', 30)

    @staticmethod
    def getTexture(path, resolution=(TEXTURE_SIZE, TEXTURE_SIZE)):
        """Gets a texture and scales it approprietly"""
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, resolution)

    def loadWallTextures(self):
        """Loads wall textures"""
        return {
            1: self.getTexture('resources/textures/block_wall.png'),
            2: self.getTexture('resources/textures/brick_wall.png'),
        }

    def renderTextures(self):
        """Renders textures in textureList"""
        textureList = sorted(
                self.game.raycasting.objectRenderList,
                key=lambda t: t[0],
                reverse=True
        )
        for depth, image, position in textureList:
            self.screen.blit(image, position)

    def drawSky(self):
        """Draws the Sky and Floor of a Map"""
        self.skyDisplacement = (
            self.skyDisplacement + 4.5 * self.game.player.relativePosition
        ) % WIDTH
        self.screen.blit(self.skyTexture, (-self.skyDisplacement, 0))
        self.screen.blit(self.skyTexture, (-self.skyDisplacement + WIDTH, 0))
        # floor
        pg.draw.rect(
            self.screen,
            GROUND_COLOR,
            (0, HALF_HEIGHT, WIDTH, HEIGHT)
        )

    def drawGameOver(self):
        """Renders game over screen"""
        self.screen.blit(self.gameOver, (0, 0))
        self.gameOverSurface = self.gameFont.render("GAME OVER", False, 'red')
        self.gameRestartSurface= self.gameOptionsFont.render("Restart (R)", False, 'red')
        self.gameExitSurface = self.gameOptionsFont.render("Quit (ESC)", False, 'red')
        self.gameOverRect = self.gameOverSurface.get_rect(midtop = (800, 100))
        self.gameRestartRect = self.gameRestartSurface.get_rect(bottomleft = (200, 700))       
        self.gameExitRect = self.gameExitSurface.get_rect(bottomright = (1400,700))

    def draw(self):
        """Calls/Executes rendering methods"""
        self.drawSky()
        self.renderTextures()
