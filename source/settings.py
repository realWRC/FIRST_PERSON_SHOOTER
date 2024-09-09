import pygame as pg
import math


# DEVELOPER SETTINGS
MODE = '3D'
TESTMODE = '3D'
LINEOFSIGHT = False
PATH_FINDING_SETTING = True

# Cheats
INFINITE_HEALTH = False

# DISPLAY SETTINGS
RES = WIDTH, HEIGHT = 1600, 900
FPS = 60
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

# GRAPHICS SETTINGS
GROUND_COLOR = (30, 30, 30)
TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

# PLAYER SETTINGS
PLAYER_POSITION = 2, 2
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_SPRINT_MULTIPLIER = 2
PLAYER_ROTATION_SPEED = 0.002
PLAYER_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 100

# GAMEPLAY SETTINGS
# Mouse
ENABLE_MOUSE = True
DISABLE_MOUSE_VISIBILITY = True
MOUSES_SENSITIVITY = 0.0003
MOUSES_MAXUMUM_RELAT = 40
MOUSES_LEFT_BORDER = 100
MOUSES_RIGHT_BORDER = WIDTH - MOUSES_LEFT_BORDER

# Key Rotation
ENABLE_KEY_ROTATION = True

# Field of View Settings
FIELD_OF_VIEW = math.pi / 3
HALF_FOV = FIELD_OF_VIEW / 2
NUMB_RAYS = WIDTH // 2
HALF_NUMB_RAYS = NUMB_RAYS // 2
ANGLE_CHANGE = FIELD_OF_VIEW / NUMB_RAYS
MAXIMUM_DEPTH = 20
SCREEN_DISTANCE = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUMB_RAYS
