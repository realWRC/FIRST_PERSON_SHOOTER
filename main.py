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
    The Game class encapsulates the core functionality of the game,
    managing the game's initialization, updates, rendering, and
    event handling. It forms the main game loop and provides a
    framework for interacting with game components, such as the
    map, player, and audio.
    """

    def __init__(self):
        """
        Initializes the game instance. This method sets up the game environment
        """
        pg.init()
        if DISABLE_MOUSE_VISIBILITY is True:
            pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.deltaTime = 1
        self.universalTrigger = False

        # Custom event that uses timer to speed up death animations
        self.universalEvent = pg.USEREVENT + 0
        pg.time.set_timer(self.universalEvent, 40)
        self.active = True
        self.victory = False
        self.gameOver = False

    def newGame(self):
        """
        Starts a new instance of the game and initializes all components
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
        """
        Updates the state of the game every frame using the core game
        components
        """
        self.player.update()
        self.raycasting.update()
        self.spriteManager.update()
        self.weapon.update()
        pg.display.flip()
        self.deltaTime = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        """
        Renders the game onto the screen. Depending on the game mode, it
        either:
            - Fills the screen with black in test mode and renders the
              map/player in a 2D representation.
            - Uses the renderer to draw the full 3D game world and the
              player's weapon.
        """
        if MODE == 'Test':
            self.screen.fill('black')
            if TESTMODE == '2D':
                self.map.testDraw()
                self.player.testDraw()
        else:
            self.renderer.draw()
            self.weapon.draw()

    def eventLoop(self):
        """
        Handles all player inputs and game events. It listens for various
        Pygame events, such as:
            - Quit events (to exit the game).
            - Keyboard inputs (such as pausing, restarting, sprinting)
            - Custom universalEvent triggers (for animations)
            - Player interaction events (e.g., firing a weapon or
              sprinting)
        """
        self.universalTrigger = False

        for event in pg.event.get():
            if event.type == pg.QUIT or\
                  (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            # Death Animation Timer Trigger
            elif event.type == self.universalEvent:
                self.universalTrigger = True

            # Shooting Event
            if self.active:
                self.player.oneShotEvent(event)

            # Pause game logic
            if event.type == pg.KEYDOWN and event.key == pg.K_p and \
                    self.gameOver is False:
                if self.active:
                    self.active = False
                else:
                    self.active = True

            # Restart game logic
            if (self.active is False or self.victory is True) and \
                    (event.type == pg.KEYDOWN and event.key == pg.K_r):
                self.gameOver = False
                self.victory = False
                self.active = True
                self.newGame()

            # Sprinting logic
            if event.type == pg.KEYDOWN and event.key == pg.K_LSHIFT:
                self.player.sprintMultiplier = 2
            if event.type == pg.KEYUP and event.key == pg.K_LSHIFT:
                self.player.sprintMultiplier = 1

    def run(self):
        """
        Runs/executes the core game loop
        """
        self.newGame()
        while True:
            self.eventLoop()
            if self.active:
                self.update()
                self.draw()
                if self.victory:
                    self.renderer.drawVictory()
            elif self.gameOver:
                self.renderer.drawGameOver()
            else:
                self.renderer.drawPauseMenu()


if __name__ == "__main__":
    game = Game()
    game.run()
