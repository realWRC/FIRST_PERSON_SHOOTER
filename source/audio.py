import pygame as pg


class Audio:
    """Controls all audio/sound effects"""

    def __init__(self, game):
        """Initialises all audio resources"""
        pg.mixer.init()
        self.path = 'resources/audio/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun_shot.mp3')