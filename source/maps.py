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

mapTwo = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, _, 1, 1, 1, 1, 1, 1, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, 1, _, _, _, _, 1, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, _, _, _, _, _, _, 1, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, _, _, _, _, _, _, 1, _, _, _, 1, 1, 1, 1, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, _, _, 1, 1, _, _, _, 1, _, _, 1, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, 1, _, _, _, _, _, _, _, 1, 1, _, 1, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, 1, _, _, _, 1, 1, 1, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, 1, 1, 1, 1, 1, 1, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, 1, _, _, _, 1, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, 1, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, 1, 1, _, _, 1, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, 1, 1, _, _, 1, 1, 1, 1, 1, 1, _, _, 1],
    [1, _, _, _, _, _, _, 1, 1, 1, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, 1, _, _, _, _, _, 1, 1, 1, 1, _, _, _, 1, 1, _, _, 1],
    [1, _, _, 1, 1, 1, 1, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, 1, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, 1, _, _, 1, _, _, 1, 1, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Map:
    """
    The Map class represents the game world map, consisting of 2D
    grid-like structure where each cell can contain different
    values representing various game elements like walls or empty
    spaces.

    Attributes:
        game (Game): An instance of the Game class, used to access
                     the game environment.
        map (list): A predefined 2D list representing the layout of
                    the game world.
        gameWorld (dict): A dictionary mapping coordinates to values
                          in the game map.
        horizontals (int): The number of horizontal rows in the map.
        verticals (int): The number of vertical columns in the map.
    """

    def __init__(self, game):
        """
        Initializes the Map class by loading the predefined map
        layout and setting up attributes for use within the game.

        Args:
            game (Game): A reference to the main Game object that
                         contains the game state and display surface.
        """
        self.game = game
        self.map = mapTwo
        self.gameWorld = {}
        self.horizontals = len(self.map)
        self.verticals = len(self.map[0])
        self.getMap()

    def getMap(self):
        """
        Populates the gameWorld dictionary with non-empty cells from the map.

        Each non-zero cell in the map is stored in the gameWorld dictionary
        with its coordinates as the key and the cell value as the value.
        """
        for y, horizontal in enumerate(self.map):
            for x, value in enumerate(horizontal):
                if value != 0:
                    self.gameWorld[(x, y)] = value

    def testDraw(self):
        """
        Draws a simple 2D visual representation of the map for testing
        purposes.

        Each non-empty cell in the gameWorld is drawn as a white rectangle
        on the screen, giving a visual overview of the game world layout.
        """
        for point in self.gameWorld:
            pg.draw.rect(
                self.game.screen,
                'white',
                (point[0] * 100, point[1] * 100, 100, 100),
                2
            )
