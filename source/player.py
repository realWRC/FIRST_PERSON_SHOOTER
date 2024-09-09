from source.settings import *
import pygame as pg
import math


class Player:
    """
    The Player class defines the player's attributes, movement, and interaction
    with the game world. It handles input from the keyboard and mouse to
    control player movement and shooting, and manages the player's health and
    collision detection.

    Attributes:
        game (Game): Reference to the main game instance.
        x, y (float): Player's position on the map.
        angle (float): Player's facing direction in radians.
        health (int): Player's health points.
        relativePosition (int): Horizontal mouse movement for aiming.
        fire (bool): Whether the player is currently firing a weapon.
        sprintMultiplier (int): Multiplier for player's speed during sprinting.
    """

    def __init__(self, game):
        """
        Initializes the Player instance, setting its position, angle, health,
        and input-related attributes.

        Args:
            game (Game): A reference to the main game instance.
        """
        self.game = game
        self.x, self.y = PLAYER_POSITION
        self.angle = PLAYER_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.relativePosition = 0
        self.fire = False
        self.killedEnemy = False
        self.sprintMultiplier = 1

    def movement(self):
        """
        Handles movement controls for the player. Movement speed is scaled
        by deltaTime to ensure consistency across frame rates. Players can
        move in all four cardinal directions (WASD) and rotate if rotation
        keys are enabled.
        """
        angleSin = math.sin(self.angle)
        angleCos = math.cos(self.angle)
        px, py = 0, 0
        speed = PLAYER_SPEED * self.sprintMultiplier * self.game.deltaTime
        speedSin = speed * angleSin
        speedCos = speed * angleCos

        buttons = pg.key.get_pressed()
        if buttons[pg.K_w]:
            px += speedCos
            py += speedSin
        if buttons[pg.K_s]:
            px += -speedCos
            py += -speedSin
        if buttons[pg.K_a]:
            px += speedSin
            py += -speedCos
        if buttons[pg.K_d]:
            px += -speedSin
            py += speedCos

        self.wallCollision(px, py)

        if ENABLE_KEY_ROTATION is True:
            if buttons[pg.K_LEFT]:
                self.angle -= PLAYER_ROTATION_SPEED * self.game.deltaTime
            if buttons[pg.K_RIGHT]:
                self.angle += PLAYER_ROTATION_SPEED * self.game.deltaTime

        self.angle %= math.tau

    def oneShotEvent(self, event):
        """
        Listens for input from the left mouse button to handle the player's
        shooting action. When the left mouse button is clicked, the player
        shoots a weapon if it's not already firing or reloading.
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.fire and\
                    not self.game.weapon.reload:
                self.game.audio.shotgun.play()
                self.fire = True
                self.game.weapon.reload = True

    def getDamage(self, damage):
        """
        Reduces the player's health by the specified damage amount.
        Triggers sound effects for player pain and checks if the player's
        health has dropped below zero, ending the game if necessary.
        """
        if MODE == 'Test' or INFINITE_HEALTH is True:
            pass
        else:
            self.health -= damage
        self.game.audio.playerPain.play()
        self.checkGame()

    def checkGame(self):
        """
        Checks whether the player's health has fallen below one. If so,
        the game is considered over, and the game over screen is displayed.
        """
        if self.health < 1:
            self.game.renderer.drawGameOver()
            self.game.active = False
            self.game.gameOver = True

    @property
    def position(self):
        """
        Returns the player's current position on the map as a tuple (x, y).
        """
        return self.x, self.y

    @property
    def mapPosition(self):
        """
        Returns the player's position on the game map in terms of tile
        coordinates.
        """
        return int(self.x), int(self.y)

    def getWallBounds(self, x, y):
        """
        Checks if the given coordinates (x, y) are within the boundaries of
        the game's world and are not occupied by a wall.
        """
        return (x, y) not in self.game.map.gameWorld

    def wallCollision(self, px, py):
        """
        Handles collision detection for the player. Prevents the player from
        passing through walls by adjusting the player's position based on
        nearby walls.
        """
        playerScale = PLAYER_SIZE_SCALE / self.game.deltaTime
        if self.getWallBounds(int(self.x + px * playerScale), int(self.y)):
            self.x += px
        if self.getWallBounds(int(self.x), int(self.y + py * playerScale)):
            self.y += py

    def mouseControl(self):
        """
        Controls the player's aim using the mouse. The player's angle is
        updated based on horizontal mouse movement, and the cursor is
        confined to the screen.
        """
        mx, my = pg.mouse.get_pos()
        if mx < MOUSES_LEFT_BORDER or mx > MOUSES_RIGHT_BORDER:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.relativePosition = pg.mouse.get_rel()[0]
        self.relativePosition = max(
                -MOUSES_MAXUMUM_RELAT,
                min(MOUSES_MAXUMUM_RELAT, self.relativePosition)
        )
        self.angle += self.relativePosition * MOUSES_SENSITIVITY *\
            self.game.deltaTime

    def testDraw(self):
        """
        Renders a simple 2D representation of the player for testing
        purposes. If the line of sight feature is enabled, it also
        draws a red line indicating the player's current view direction.
        """
        if LINEOFSIGHT is True:
            pg.draw.line(
                self.game.screen, "red", (self.x * 100, self.y * 100),
                (
                    self.x * 100 + WIDTH * math.cos(self.angle),
                    self.y * 100 + WIDTH * math.sin(self.angle)
                ),
                2
            )
        pg.draw.circle(
            self.game.screen,
            'green',
            (self.x * 100, self.y * 100),
            15
        )

    def update(self):
        """
        Updates the player's state in each frame. This includes handling
        movement, mouse input, and updating the player's position on the
        map.
        """
        self.movement()
        self.mouseControl()
        if self.killedEnemy == True:
            print(self.game.spriteManager.enemyHealthRecoupe)
            self.health += self.game.spriteManager.enemyHealthRecoupe
            self.killedEnemy = False
        if self.health > PLAYER_MAX_HEALTH:
            self.health = PLAYER_MAX_HEALTH
