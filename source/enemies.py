from source.sprites import *
from random import random, randint


class Enemy(AnimatedSprite):
    """Creates and controls enemies"""

    def __init__(
            self,
            game,
            position=(4, 4),
            scale=0.8,
            change=0.27,
            duration=180,
            path='resources/sprites/enemies/trooper/0.png'
    ):
        """Initialises the enemy class"""
        super().__init__(game, position, scale, change, duration, path)
        self.attackAnimation = self.getFrames(self.path + '/attack')
        self.deathAnimation = self.getFrames(self.path + '/death')
        self.idleAnimtion = self.getFrames(self.path + '/idle')
        self.painAnimation = self.getFrames(self.path + '/pain')
        self.searchAnimation = self.getFrames(self.path + '/search')
        self.attackRange = randint(3, 5)
        self.movementSpeed = 0.04
        self.size = 20
        self.health = 100
        self.enemyDamage = 10
        self.percision = 0.15
        self.alive = True
        self.pain = False
        self.sightLineCheker = False
        self.animationFrameCounter = 0
        self.searchActivate = False

    def update(self):
        self.durationCheck()
        self.getSprite()