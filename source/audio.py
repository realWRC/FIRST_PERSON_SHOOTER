import pygame as pg


class Audio:
    """
    The Audio class is responsible for managing all in-game sound effects,
    including loading and playing audio resources such as player and enemy
    sounds.

    Core Attributes:
        game (Game): A reference to the main Game object.
        path (str): The path to the folder where audio files are stored.
    """

    def __init__(self, game):
        """
        Initializes the Audio class by setting up the audio system and loading
        various sound effects. The Pygame mixer is initialized to handle the
        playback of audio files.

        Args:
            game (Game): A reference to the main Game object for context.
        """
        pg.mixer.init()
        self.path = 'resources/audio/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun_shot.wav')
        self.enemyPain = pg.mixer.Sound(self.path + 'enemy_pain.wav')
        self.enemyDeath = pg.mixer.Sound(self.path + 'enemy_death.wav')
        self.enemyFire = pg.mixer.Sound(self.path + 'enemy_attack.wav')
        self.playerPain = pg.mixer.Sound(self.path + 'player_pain.wav')
