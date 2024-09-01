import pygame as pg


class Audio:
    """Controls all audio/sound effects"""

    def __init__(self, game):
        """Initialises all audio resources"""
        pg.mixer.init()
        self.path = 'resources/audio/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun_shot.wav')
        self.enemyPain = pg.mixer.Sound(self.path + 'enemy_pain.wav')
        self.enemyDeath = pg.mixer.Sound(self.path + 'enemy_death.wav')
        self.enemyFire = pg.mixer.Sound(self.path + 'enemy_attack.wav')
        self.playerPain = pg.mixer.Sound(self.path + 'player_pain.wav')