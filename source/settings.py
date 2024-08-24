import pygame as pg

def calculateResolution(scale=1):
    """Calculates screen resolution for dynamic screen sizing"""
    pg.init()
    screen = pg.display.Info()
    pg.quit()
    return int(screen.current_w * scale), int(screen.current_h * scale)

#SCREEN RESOLUTION
RES = WIDTH, HEIGHT = 1600, 900
FPS = 60