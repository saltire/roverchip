import os
import sys

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
        self.run(Menu(self, levels))
    
    
    def init_window(self, (width, height)):
        """Initialize the game window. Called at beginning, and every time
        the window is resized."""
        pygame.display.set_mode((width, height), pygame.RESIZABLE).fill((0, 0, 0))
        
        
    def run(self, screen):
        """Run this screen, checking status after each frame."""
        while True:
            # update display and tick the clock
            screen.resize_view()
            screen.draw_frame()
            pygame.display.update()
            elapsed = float(self.clock.tick(60))
            
            keys = []
            for event in pygame.event.get():
                # close window
                if event.type == pygame.QUIT:
                    sys.exit()
                    
                # resize window
                elif event.type == pygame.VIDEORESIZE:
                    self.init_window(event.size)
                    
                # get keypresses
                elif event.type == pygame.KEYDOWN:
                    keys.append((event.key, 1))
                elif event.type == pygame.KEYUP:
                    keys.append((event.key, 0))
                    
            # run a frame of this screen
            if screen.run_frame(elapsed, keys) == 'quit':
                return
            
        
