import pygame as pg
import sys
from source.raycasting import *
from source.settings import *
from source.maps import *
from source.player import *
from source.renderer import *
from source.sprites import *
from source.spritemanager import *
from source.weapons import *
from source.audio import *
from source.pathfinding import *


class Game:
    """
    The class Game defines all methods that form the core game loop
    """

    def __init__(self):
        """Initi Game Instance"""
        pg.init()
        if DISABLE_MOUSE_VISIBILITY is True:
            pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.deltaTime = 1
        self.universalTrigger = False
        self.universalEvent = pg.USEREVENT + 0
        pg.time.set_timer(self.universalEvent, 40)
        self.active = True
        self.victory = False
        self.gameOver = False

    def newGame(self):
        """
        Starts a new instance of Game:
            self.map - creates new map on every game
        """
        self.map = Map(self)
        self.player = Player(self)
        self.renderer = Renderer(self)
        self.raycasting = RayCasting(self)
        self.spriteManager = SpriteManager(self)
        self.weapon = Weapon(self)
        self.audio = Audio(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        """Updates the state of the game"""
        self.player.update()
        self.raycasting.update()
        self.spriteManager.update()
        self.weapon.update()
        pg.display.flip()
        self.deltaTime = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        """Renders the game in the window"""
        if MODE == 'Test':
            self.screen.fill('black')
            if TESTMODE == '2D':
                self.map.testDraw()
                self.player.testDraw()
        else:
            self.renderer.draw()
            self.weapon.draw()

    def eventLoop(self):
        self.universalTrigger = False
        """Listens for keyboard to exit the game"""
        for event in pg.event.get():
            if event.type == pg.QUIT or\
                  (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.universalEvent:
                self.universalTrigger = True
            if self.active:
                self.player.oneShotEvent(event)
            
            # Pause Game
            if event.type == pg.KEYDOWN and event.key == pg.K_p and self.gameOver == False:
                if self.active:
                    self.active = False
                else:
                    self.active = True
            if (self.active == False or self.victory == True) and (event.type == pg.KEYDOWN and event.key == pg.K_r):
                self.active = True
                self.newGame()
            
            # Sprinting
            if event.type == pg.KEYDOWN and event.key == pg.K_LSHIFT:
                self.player.sprintMultiplier = 2
            if event.type == pg.KEYUP and event.key == pg.K_LSHIFT:
                self.player.sprintMultiplier = 1
                

    def run(self):
        """Executes the game loop"""
        self.newGame()
        while True:
            self.eventLoop()
            if self.active:
                self.update()
                self.draw()
                if self.victory:
                    self.renderer.drawVictory()
            else:
                self.renderer.drawPauseMenu()


if __name__ == "__main__":
    game = Game()
    game.run()
