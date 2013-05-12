import os

import pygame

import config
from roverchip.game import Game
from roverchip.menu import MainMenu
from roverchip.tiledmap import TiledMap
from roverchip.window import Window


if __name__ == '__main__':
    pygame.init()
    pygame.key.set_repeat(1, config.keyrepeat)
    
    levels = TiledMap(config.levelpath).get_levels()
    
    window = Window(config.windowsize)
    window.run(MainMenu(window, levels))
    