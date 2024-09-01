from source.sprites import *
from source.enemies import *


class SpriteManager:
    """Controls which sprites are used"""

    def __init__(self, game):
        """Initialises SpriteManager class"""
        self.game = game
        self.spriteList = []
        self.enemyList = []
        self.enemyPositions = {}
        staticSpritePath = 'resources/sprites/static/'
        animatedSpritePath = 'resources/sprites/animated/'
        self.enemySpritePath = 'resources/sprites/enemies/'
        addSprite = self.addSprite
        addEnemy = self.addEnemy

        addSprite(Sprite(game))
        addSprite(AnimatedSprite(game))

        addEnemy(Enemy(game))
        addEnemy(Enemy(game, position=(3, 4)))

    def addSprite(self, sprite):
        """Adds given sprite to sprite list"""
        self.spriteList.append(sprite)

    def addEnemy(self, npc):
        """Adds given enemy to enemy list"""
        self.enemyList.append(npc)

    def update(self):
        """Calls update method for every sprite in spriteList"""
        self.enemyPositions = set()
        for enemy in self.enemyList:
            if enemy.alive:
                self.enemyPositions.add(enemy.enemyMapPosition)

        for sprite in self.spriteList:
            sprite.update()

        for enemy in self.enemyList:
            enemy.update()
