import os

import pygame

from menu import Menu
from tiledmap import TiledMap


class Window:
    def __init__(self, levelpath='levels/*.tmx', size=(800, 480)):
        # init pygame variables
        pygame.init()
        self.init_window(size)
        pygame.key.set_repeat(1, 100)
        
        # init properties
        self.view = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.path = os.path.dirname(__file__)

        # init levels
        levels = TiledMap(os.path.join(self.path, levelpath)).get_levels()

        # run the menu screen
        Menu(self, levels).run()
    
    
    def init_window(self, (width, height)):
        """Initialize the game window. Called at beginning, and every time
        the window is resized."""
        pygame.display.set_mode((width, height), pygame.RESIZABLE).fill((0, 0, 0))
        
