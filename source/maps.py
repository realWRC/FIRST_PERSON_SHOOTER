import pygame as pg

_ = 0
mapOne = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, 2, 2, 2, _, _, 1, 1, 1, 1, _, _, 1],
    [1, _, _, _, _, _, 2, _, _, 1, _, _, _, _, _, 1],
    [1, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, 2, 2, 2, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, 1, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Map:
    """Defines the class Map"""

    def __init__(self, game):
        """Initialises and a Map"""
        self.game = game
        self.map = mapOne
        self.gameWorld = {}
        self.getMap()
        self.original_width, self.original_height = self.game.screen.get_size()

    def getMap(self):
        """Constructes the gameWorld"""
        for j, row in enumerate(self.map):
            for i, value in enumerate(row):
                if value != 0:
                    self.gameWorld[(i, j)] = value

    def testDraw(self):
        """Draws the Map for testing"""
        for point in self.gameWorld:
            pg.draw.rect(
                self.game.screen,
                'darkgray',
                (point[0] * 100, point[1] * 100, 100, 100),
                2
            )
