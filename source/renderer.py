import pygame as pg
from source.settings import *


class Renderer:
    """Defines methods for rendering objects"""

    def __init__(self, game):
        """Initalises object render"""
        self.game = game
        self.screen = game.screen
        self.wallTexture = self.loadWallTexture()

    @staticmethod
    def getTexture(location, resolution=(TEXTURESIZE, TEXTURESIZE)):
        """Gets a texture and scales it approprietly"""
        texture = pg.image.load(location).convert_alpha()
        return pg.transform.scale(texture, resolution)
    
    def loadWallTexture(self):
        """Loads wall textures"""
        return {
            1: self.getTexture('resources/textures/block_wall.png'),
            2: self.getTexture('resources/textures/brick_wall.png'),
        }