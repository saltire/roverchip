import os
import sys

import pygame

from menu import Menu
from tiledmap import TiledMap


class Window:
    def __init__(self, levelpath='levels/*.tmx', size=(800, 480)):
        # init pygame variables
        pygame.init()
        pygame.key.set_repeat(1, 100)
        
        # init properties
        self.clock = pygame.time.Clock()
        self.path = os.path.dirname(__file__)
        self.min_size = 200, 120
        self.screens = []
        
        self.init_window(size)

        # init levels and run the menu screen
        levels = TiledMap(os.path.join(self.path, levelpath)).get_levels()
        self.run(Menu(self, levels))
    
    
    def init_window(self, size):
        """Initialize the game window. Called at beginning, and every time
        the window is resized."""            
        # enforce minimum size
        (mw, mh), (w, h) = self.min_size, size
        if w < mw or h < mh:
            size = self.min_size
                
        last_size = self.view.get_size() if hasattr(self, 'view') else None
        
        # init view
        self.view = pygame.display.set_mode(size, pygame.RESIZABLE)
        
        # if resized, repaint background and run screen hook
        if size != last_size:
            self.view.fill((0, 0, 0))
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
            
        
