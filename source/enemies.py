from source.sprites import *
from random import random, randint


class Enemy(AnimatedSprite):
    """
    The Enemy class defines the behavior, animations, and interactions
    of the enemies in the game. It extends the AnimatedSprite class
    and adds specific logic for movement, attacking the player,
    detecting sightlines, and handling health and death states.

    Attributes:
        game (Game): A reference to the main game instance.
        position (tuple): The initial position of the enemy on the map.
        scale (float): The size scaling factor for the enemy sprite.
        change (float): Animation speed change factor.
        duration (int): Duration for enemy animation cycles.
        path (str): Path to the enemy sprite resources.
        attackAnimation (list): Frames for the enemy attack animation.
        deathAnimation (list): Frames for the enemy death animation.
        idleAnimation (list): Frames for the enemy idle animation.
        painAnimation (list): Frames for the enemy pain animation.
        searchAnimation (list): Frames for the enemy search animation.
        attackRange (int): Distance within which the enemy can attack
        the player.
        movementSpeed (float): Speed of the enemy's movement.
        size (int): The size used for collision detection.
        health (int): Enemy's health points.
        enemyDamage (int): Damage dealt by the enemy to the player.
        percision (float): Accuracy of the enemy's attack.
        alive (bool): Whether the enemy is alive.
        pain (bool): Whether the enemy is in pain (after being hit).
        sightLineCheker (bool): Flag indicating whether the player is in sight.
        animationFrameCounter (int): Tracks the frame of the death animation.
        searchActivate (bool): Flag for enabling the search animation.
    """

    def __init__(
            self,
            game,
            position=(4, 4),
            scale=0.8,
            change=0.27,
            duration=180,
            path='resources/sprites/enemies/trooper/0.png'
    ):
        """
        Initializes the Enemy class by loading animations, setting the enemy's
        stats, and defining initial parameters such as position, speed, and
        health.

        Args:
            game (Game): Reference to the main game object.
            position (tuple): Initial position of the enemy.
            scale (float): Scaling factor for the enemy sprite.
            change (float): Animation change rate.
            duration (int): Animation duration cycle.
            path (str): Path to the enemy sprite directory.
        """
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
        """
        Defines the core logic for the enemy, including sightline detection,
        movement, attacking, and handling pain and death animations.
        """
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
        """
        Plays the pain animation when the enemy is injured and resets the
        pain flag once the animation is complete.
        """
        self.animate(self.painAnimation)
        if self.animationTrigger:
            self.pain = False

    def animateDeath(self):
        """
        Plays the death animation when the enemy's health reaches zero,
        advancing through the animation frames until completion.
        """
        if not self.alive:
            if self.game.universalTrigger and self.animationFrameCounter\
                    < len(self.deathAnimation) - 1:
                self.deathAnimation.rotate(-1)
                self.image = self.deathAnimation[0]
                self.animationFrameCounter += 1

    def shotHitDetection(self):
        """
        Detects if the player's shot hits the enemy by checking whether
        the player is firing and whether the enemy is within the player's
        line of sight. If hit, the enemy takes damage.
        """
        if self.sightLineCheker and self.game.player.fire:
            if HALF_WIDTH - self.spriteHalfWidth < self.screenX\
                    < HALF_WIDTH + self.spriteHalfWidth:
                self.game.audio.enemyPain.play()
                self.game.player.fire = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.checkHealth()

    def checkHealth(self):
        """
        Checks the enemy's health, and if it drops below 1, the enemy is
        considered dead, triggering the death animation and sound effect.
        """
        if self.health < 1:
            self.alive = False
            self.game.audio.enemyDeath.play()

    def attack(self):
        """
        Executes the enemy's attack logic. If the enemy is within attack
        range and the animation is triggered, the enemy fires at the player,
        dealing damage based on a random precision check.
        """
        if self.animationTrigger:
            if MODE != 'Test':
                self.game.audio.enemyFire.play()
                if random() < self.percision:
                    self.game.player.getDamage(self.enemyDamage)

    @property
    def enemyMapPosition(self):
        """Returns the enemy's current position on the game map grid."""
        return int(self.x), int(self.y)

    def getWallBounds(self, x, y):
        """
        Checks whether a given coordinate on the map is a wall or an open
        space.

        Args:
            x (int): X coordinate to check.
            y (int): Y coordinate to check.

        Returns:
            bool: True if the given position is not a wall, False otherwise.
        """
        return (x, y) not in self.game.map.gameWorld

    def rayCastSightLine(self):
        """
        Performs a raycast from the enemy's position to the player's position
        to detect whether the player is within line of sight without any walls
        blocking the view.

        Returns:
            bool: True if the player is in sight, False otherwise.
        """
        if self.game.player.mapPosition == self.enemyMapPosition:
            return True

        vertWallDist, hortWallDist = 0, 0
        vertPlayerDist, hortPlayerDist = 0, 0
        px, py = self.game.player.position
        mapX, mapY = self.game.player.mapPosition
        rayAngle = self.thetaAngle
        raySin = math.sin(rayAngle)
        rayCos = math.cos(rayAngle)

        # horizontals
        yHort, dy = (mapY + 1, 1) if raySin > 0 else (mapY - 1e-6, -1)
        depthHort = (yHort - py) / raySin
        xHort = px + depthHort * rayCos
        deltaChange = dy / raySin
        dx = deltaChange * rayCos

        for i in range(MAXIMUM_DEPTH):
            tileHort = int(xHort), int(yHort)
            if tileHort == self.enemyMapPosition:
                hortPlayerDist = depthHort
                break
            if tileHort in self.game.map.gameWorld:
                hortWallDist = depthHort
                break
            xHort += dx
            yHort += dy
            depthHort += deltaChange

        # verticals
        xVert, dx = (mapX + 1, 1) if rayCos > 0 else (mapX - 1e-6, -1)
        depthVert = (xVert - px) / rayCos
        yVert = py + depthVert * raySin
        deltaChange = dx / rayCos
        dy = deltaChange * raySin

        for i in range(MAXIMUM_DEPTH):
            tileVert = int(xVert), int(yVert)
            if tileVert == self.enemyMapPosition:
                vertPlayerDist = depthVert
                break
            if tileVert in self.game.map.gameWorld:
                vertWallDist = depthVert
                break
            xVert += dx
            yVert += dy
            depthVert += deltaChange

        playerDistance = max(vertPlayerDist, hortPlayerDist)
        wallDistance = max(vertWallDist, hortWallDist)

        if 0 < playerDistance < wallDistance or not wallDistance:
            return True
        return False

    def movement(self):
        """
        Moves the enemy towards the player's position. Depending on the game's
        pathfinding setting, the enemy can either follow a pre-calculated route
        or move directly toward the player.
        """
        if PATH_FINDING_SETTING:
            nextPosition = self.game.pathfinding.getRoute(
                    self.enemyMapPosition,
                    self.game.player.mapPosition
            )
        else:
            nextPosition = self.game.player.mapPosition
        nextPositionX, nextPositionY = nextPosition

        if MODE == 'Test' and TESTMODE == '2D' and \
                PATH_FINDING_SETTING is True:
            pg.draw.rect(
                    self.game.screen,
                    'green',
                    (100 * nextPositionX, 100 * nextPositionY, 100, 100)
            )
        if nextPosition not in self.game.spriteManager.enemyPositions:
            angle = math.atan2(
                    nextPositionY + 0.5 - self.y,
                    nextPositionX + 0.5 - self.x
            )
            ex = math.cos(angle) * self.movementSpeed
            ey = math.sin(angle) * self.movementSpeed
            self.wallCollusion(ex, ey)

    def wallCollusion(self, dx, dy):
        """
        Checks for wall collisions and updates the enemy's position
        accordingly.

        Args:
            dx (float): Change in the enemy's X position.
            dy (float): Change in the enemy's Y position.
        """
        if self.getWallBounds(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.getWallBounds(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def update(self):
        """
        Updates the enemy's state by checking animations, executing
        logic, and drawing test visuals if in debug mode.
        """
        self.durationCheck()
        self.getSprite()
        self.enemyLogic()
        self.testDraw()

    def testDraw(self):
        """
        Draws visual elements for debugging, such as the enemy's
        position and sightline, when the game is in test mode.
        """
        if MODE == 'Test' and TESTMODE == '2D':
            pg.draw.circle(
                    self.game.screen,
                    'red',
                    (100 * self.x, 100 * self.y),
                    15
            )
            if self.rayCastSightLine():
                pg.draw.line(
                    self.game.screen,
                    'purple',
                    (100 * self.game.player.x, 100 * self.game.player.y),
                    (100 * self.x, 100 * self.y),
                    2
                )
