import os
import sys

import pygame

from config import Config
from menu import MainMenu
from tiledmap import TiledMap


class Window:
    def __init__(self, configpath='config'):
        # init config
        self.path = os.path.dirname(__file__)
        self.config = Config(os.path.join(self.path, configpath), 'roverchip')
        
        # init pygame variables
        pygame.init()
        pygame.key.set_repeat(1, self.config.getint('keyrepeat'))
        self.clock = pygame.time.Clock()
        
        # init screens and window
        self.screens = []
        self.init_window(self.config.getints('windowsize'))

        # init levels and run the menu screen
        levelpath = self.config.get('levelpath')
        levels = TiledMap(os.path.join(self.path, levelpath)).get_levels()
        self.run(MainMenu(self, levels))
    
    
    def init_window(self, size):
        """Initialize the game window. Called at beginning, and every time
        the window is resized."""            
        # enforce minimum size
        minsize = self.config.getints('minsize')
        (mw, mh), (w, h) = minsize, size
        if w < mw or h < mh:
            size = minsize
                
        # init view, repaint background and run screen hook
        self.view = pygame.display.set_mode(size, pygame.RESIZABLE)
        for screen in self.screens:
            screen.resize_view(size)
        
        
    def run(self, screen):
        """Run this screen, checking status after each frame."""
        self.screens.append(screen)
        
        while True:
            # update display and tick the clock
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
                self.screens.pop()
                return
            
        
