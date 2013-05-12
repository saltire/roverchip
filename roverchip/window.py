import sys

import pygame

import config


class Window:
    def __init__(self, size):
        # init config
        self.clock = pygame.time.Clock()
        self.screens = []

        self.init_window(size)
    
    
    def init_window(self, size):
        """Initialize the game window. Called at beginning, and every time
        the window is resized."""            
        # enforce minimum size
        (mw, mh), (w, h) = config.minsize, size
        if w < mw or h < mh:
            size = mw, mh
                
        # init view, repaint background and run screen hook
        self.view = pygame.display.set_mode(size, pygame.RESIZABLE)
        for screen in self.screens:
            screen.set_view(self.view)
        
        
    def run(self, screen):
        """Run this screen, checking status after each frame."""
        self.screens.append(screen)
        screen.set_view(self.view)
        
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
            nextscreen = screen.run_frame(elapsed, keys)
            
            if nextscreen is False:
                # return to the previous screen on the stack
                self.screens.pop()
                return
            
            elif nextscreen is not None:
                # add a new screen to the stack
                self.run(nextscreen)
            
        
