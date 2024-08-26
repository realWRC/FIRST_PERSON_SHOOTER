import pygame as pg
import math

def calculateResolution(scale=1):
    """Calculates screen resolution for dynamic screen sizing"""
    pg.init()
    screen = pg.display.Info()
    pg.quit()
    return int(screen.current_w * scale), int(screen.current_h * scale)

# GAME SETTINGS
# MODE RENDER IN 3D IF TRUE
MODE = False
LINEOFSIGHT = False

# SCREEN SETTINGS
RES = WIDTH, HEIGHT = 1600, 900
FPS = 60
HALFWIDTH = WIDTH // 2
HALFHEIGHT = HEIGHT // 2

# PLAYER MOVEMENT SETTINGS
PLAYER_POSITION = 1.5, 5
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROTATION_SPEED = 0.002

# PLAYER FIELD OF VIEW SETTINGS
FOV = math.pi / 3
HFOV = FOV / 2
RAYS = WIDTH // 2
HRAYS = RAYS // 2
ANGLECHANGE = FOV / RAYS
MAX_DEPTH = 20
SCREENDISTANCE = HALFWIDTH / math.tan(HFOV)
SCALE = WIDTH // RAYS
