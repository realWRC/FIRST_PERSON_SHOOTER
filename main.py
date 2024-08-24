import pygame as pg
import sys
from source.settings import *
from source.maps import *


class Game:
    """
    The class Game defines all methods that form the core game loop
    """

    def __init__(self):
        """Initialises Game Instance"""
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.newGame()

    def newGame(self):
        """
        Starts a new instance of Game:
            self.map - creates new map on every game
        """
        self.map = Map(self)

    def update(self):
        """Updates the state of the game"""
        pg.display.flip()
        self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        """Renders the game in the window"""
        self.screen.fill('black')
        self.map.draw()

    def listenEvents(self):
        """Listens for keyboard to exit the game"""
        for event in pg.event.get():
            if event.type == pg.QUIT or\
                  (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        """Executes the game loop"""
        while True:
            self.listenEvents()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()