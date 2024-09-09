from source.sprites import *
from source.enemies import *


class SpriteManager:
    """
    The SpriteManager class manages all the sprites and enemies in the
    game, including static and animated sprites. It keeps track of sprite
    updates and enemy states, and determines when the player has achieved
    victory by checking if all enemies are defeated.

    Attributes:
        game (Game): Reference to the main game instance.
        spriteList (list): A list containing all the sprites in the game.
        enemyList (list): A list containing all the enemies in the game.
        enemyNumber (int): The number of enemies currently in the game.
        enemyPositions (set): A set of the positions of all active enemies.
        enemySpritePath (str): File path to the enemy sprite resources.
    """

    def __init__(self, game):
        """
        Initializes the SpriteManager by setting up lists for sprites and
        enemies, loading static and animated sprites, and adding enemies to
        the game world.

        Args:
            game (Game): A reference to the main game instance.
        """
        self.game = game
        self.spriteList = []
        self.enemyList = []
        self.enemyNumber = len(self.enemyList)
        self.enemyPositions = {}
        self.enemyHealthRecoupe = 0
        staticSpritePath = 'resources/sprites/static/'
        animatedSpritePath = 'resources/sprites/animated/'
        self.enemySpritePath = 'resources/sprites/enemies/'
        addSprite = self.addSprite
        addEnemy = self.addEnemy

        # Stationary Sprites
        addSprite(Sprite(game))
        addSprite(AnimatedSprite(game))
        addSprite(Arachnotron(game))

        # Enemies
        addEnemy(Enemy(game))
        addEnemy(DeathKnight(game))

    def addSprite(self, sprite):
        """
        Adds a given sprite to the list of sprites. The sprite can be static
        or animated.

        Args:
            sprite (Sprite): The sprite object to be added to the sprite list.
        """
        self.spriteList.append(sprite)

    def addEnemy(self, npc):
        """
        Adds a given enemy to the list of enemies. This method is responsible
        for managing enemy placement and their inclusion in the game world.

        Args:
            npc (Enemy): The enemy object to be added to the enemy list.
        """
        self.enemyList.append(npc)

    def update(self):
        """
        Updates the state of all sprites and enemies. It checks if enemies
        are alive, updates their positions, and updates each sprite and
        enemy in the game. If all enemies are defeated, the player wins
        the game.
        """
        self.enemyPositions = set()
        enemiesAlive = 0
        for enemy in self.enemyList:
            if enemy.alive:
                self.enemyPositions.add(enemy.enemyMapPosition)
                enemiesAlive += 1

        for sprite in self.spriteList:
            sprite.update()

        for enemy in self.enemyList:
            enemy.update()

        if enemiesAlive == 0:
            # self.game.active = False
            self.game.victory = True
