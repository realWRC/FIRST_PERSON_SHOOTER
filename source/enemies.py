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

    def enemyLogic(self):
        if self.alive:
            self.sightLineCheker = self.rayCastSightLine()
            
            self.shotHitDetection()
            if self.pain:
                self.animatePain()
            elif self.sightLineCheker:
                self.searchActivate = True
                if self.distance < self.attackRange:
                    self.animate(self.attackAnimation)
                    self.attack()
                else:
                    self.animate(self.searchAnimation)
                    self.movement()
            elif self.searchActivate:
                self.animate(self.searchAnimation)
                self.movement()
            else:
                self.animate(self.idleAnimtion)
        else:
            self.animateDeath()
    
    def animatePain(self):
        self.animate(self.painAnimation)
        if self.animationTrigger:
            self.pain = False
    
    def animateDeath(self):
        if not self.alive:
            if self.game.universalTrigger and self.animationFrameCounter < len(self.deathAnimation) - 1:
                self.deathAnimation.rotate(-1)
                self.image = self.deathAnimation[0]
                self.animationFrameCounter += 1

    def update(self):
        self.durationCheck()
        self.getSprite()
        self.enemyLogic()
        self.testDraw()
