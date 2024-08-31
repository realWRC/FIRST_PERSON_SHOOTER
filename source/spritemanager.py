from source.sprites import *


class SpriteManager:
    """Controls which sprites are used"""

    def __init__(self, game):
        """Initialises SpriteManager class"""
        self.game = game
        self.spriteList = []
        staticSpritePath = 'resources/sprites/static/'
        animatedSpritePath = 'resources/sprites/animated/'
        addSprite = self.addSprite

        addSprite(Sprite(game))
        addSprite(AnimatedSprite(game))

    def addSprite(self, sprite):
        """Adds given sprite to sprite list"""
        self.spriteList.append(sprite)

    def update(self):
        """Calls update method for every sprite in spriteList"""
        for sprite in self.spriteList:
            sprite.update()
