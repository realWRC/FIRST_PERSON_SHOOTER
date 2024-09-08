import pygame as pg
from source.settings import *


class Renderer:
    """
    The Renderer class handles all graphical rendering for the game, including
    drawing textures, the sky, and floor, as well as the game's UI elements
    like stats, game over screens, pause menus, and victory screens.
    """

    def __init__(self, game):
        """
        Initializes the Renderer class by loading wall textures, setting up the
        sky texture, and preparing fonts for UI elements like game over screens
        and menus.

        Args:
            game (Game): A reference to the main game object.
        """
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
        self.gameFont = pg.font.Font('resources/fonts/Halo3.ttf', 150)
        self.gameOptionsFont = pg.font.Font('resources/fonts/Halo3.ttf', 80)

    @staticmethod
    def getTexture(path, resolution=(TEXTURE_SIZE, TEXTURE_SIZE)):
        """
        Loads a texture from the specified file path and scales it to the
        provided resolution.

        Args:
            path (str): The file path to the texture.
            resolution (tuple): The resolution to scale the texture to.

        Returns:
            Surface: The scaled texture as a Pygame Surface.
        """
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, resolution)

    def loadWallTextures(self):
        """
        Loads the textures used for rendering walls in the game. The
        textures are stored in a dictionary with numeric keys corresponding
        to different types of walls.

        Returns:
            dict: A dictionary mapping wall types to their textures.
        """
        return {
            1: self.getTexture('resources/textures/block_wall.png'),
            2: self.getTexture('resources/textures/brick_wall.png'),
        }

    def renderTextures(self):
        """
        Renders all textures in the textureList by sorting them based on
        depth, ensuring that objects farther from the player are rendered
        first. This ensures proper layering of textures.
        """
        textureList = sorted(
                self.game.raycasting.objectRenderList,
                key=lambda t: t[0],
                reverse=True
        )
        for depth, image, position in textureList:
            self.screen.blit(image, position)

    def drawSky(self):
        """
        Draws the sky and the floor of the map. The sky texture is displaced
        horizontally based on the player's relative position to simulate
        movement. The floor is drawn as a rectangle beneath the horizon.
        """
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
        """
        Renders the game over screen with options to restart or quit. It
        displays a "GAME OVER" message and provides interactive options for
        the player.
        """
        # self.screen.blit(self.gameOver, (0, 0))
        self.gameOverSurface = self.gameFont.render(
                "GAME OVER", False, 'red'
        )
        self.gameRestartSurface = self.gameOptionsFont.render(
                "Restart (R)", False, 'red'
        )
        self.gameExitSurface = self.gameOptionsFont.render(
                "Quit (ESC)", False, 'red'
        )
        self.gameOverRect = self.gameOverSurface.get_rect(
                midtop=(800, 100)
        )
        self.gameRestartRect = self.gameRestartSurface.get_rect(
                bottomleft=(200, 700)
        )
        self.gameExitRect = self.gameExitSurface.get_rect(
                bottomright=(1400, 700)
        )
        self.screen.blit(self.gameOverSurface, self.gameOverRect)
        self.screen.blit(self.gameRestartSurface, self.gameRestartRect)
        self.screen.blit(self.gameExitSurface, self.gameExitRect)
        pg.display.update(self.gameOverRect)
        pg.display.update(self.gameRestartRect)
        pg.display.update(self.gameExitRect)

    def drawStats(self):
        """
        Renders the player's health as a percentage on the top left corner
        of the screen. The health is displayed in red text and updates each
        frame.
        """
        self.game.player.health
        self.playerHealthSurface = self.gameOptionsFont.render(
                f"{(self.game.player.health/PLAYER_MAX_HEALTH) * 100}%",
                False,
                'red'
        )
        self.playerHealthRect = self.playerHealthSurface.get_rect(
                topleft=(20, 20)
        )
        self.screen.blit(self.playerHealthSurface, self.playerHealthRect)
        pg.display.update(self.playerHealthRect)

    def drawPauseMenu(self):
        """
        Renders the pause menu, displaying a "PAUSE MENU" message and options
        to restart the game or quit to the main menu.
        """
        self.gamePauseSurface = self.gameFont.render(
                "PAUSE MENU", False, 'red'
        )
        self.gameRestartSurface = self.gameOptionsFont.render(
                "Restart (R)", False, 'red'
        )
        self.gameExitSurface = self.gameOptionsFont.render(
                "Quit (ESC)", False, 'red'
        )
        self.gamePauseRect = self.gamePauseSurface.get_rect(
                midtop=(800, 100)
        )
        self.gameRestartRect = self.gameRestartSurface.get_rect(
                bottomleft=(200, 700)
        )
        self.gameExitRect = self.gameExitSurface.get_rect(
                bottomright=(1400, 700)
        )
        self.screen.blit(self.gamePauseSurface, self.gamePauseRect)
        self.screen.blit(self.gameRestartSurface, self.gameRestartRect)
        self.screen.blit(self.gameExitSurface, self.gameExitRect)
        pg.display.update(self.gamePauseRect)
        pg.display.update(self.gameRestartRect)
        pg.display.update(self.gameExitRect)

    def drawVictory(self):
        """
        Renders the victory screen with a "Victory" message and options to
        restart or quit. This is displayed when the player successfully
        completes the game.
        """
        self.gameVictorySurface = self.gameFont.render(
                "Victory", False, 'red'
        )
        self.gameRestartSurface = self.gameOptionsFont.render(
                "Restart (R)", False, 'red'
        )
        self.gameExitSurface = self.gameOptionsFont.render(
                "Quit (ESC)", False, 'red'
        )
        self.gameVictoryRect = self.gameVictorySurface.get_rect(
                midtop=(800, 100)
        )
        self.gameRestartRect = self.gameRestartSurface.get_rect(
                bottomleft=(200, 700)
        )
        self.gameExitRect = self.gameExitSurface.get_rect(
                bottomright=(1400, 700)
        )
        self.screen.blit(self.gameVictorySurface, self.gameVictoryRect)
        self.screen.blit(self.gameRestartSurface, self.gameRestartRect)
        self.screen.blit(self.gameExitSurface, self.gameExitRect)
        pg.display.update(self.gameVictoryRect)
        pg.display.update(self.gameRestartRect)
        pg.display.update(self.gameExitRect)

    def draw(self):
        """
        Calls the appropriate rendering methods to display the game visuals,
        including the sky, textures, and player stats. This method is the
        main draw loop for the game.
        """
        self.drawSky()
        self.renderTextures()
        self.drawStats()
