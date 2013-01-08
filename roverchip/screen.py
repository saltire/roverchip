import sys

import pygame


class Screen:
    def __init__(self, window):
        """Draws the initial frame. Make sure to initialize any variables needed
        to draw before calling this method from a subclass."""
        self.window = window
        self.last_windowsize = None
        
        
    def run(self):
        """Run this screen, checking status after each frame."""
        while True:
            # update display and tick the clock
            self.resize_view()
            self.draw_frame()
            pygame.display.update()
            elapsed = float(self.window.clock.tick(60))
            
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
            if self.run_frame(elapsed, keys) == 'quit':
                return
            
        
    def run_frame(self, elapsed, keys):
        """Run a single frame for this type of screen."""
        return None

    
    def resize_view(self):
        """Runs once per frame. If window size has changed, reinitialize
        the view and any elements within that need to be resized."""
        # check if the window size has changed
        windowsize = self.window.view.get_size()
        if windowsize != self.last_windowsize:
            self.last_windowsize = windowsize
        
            # initialize view using rect from child class, run hook
            self.view = self.window.view.subsurface(self.find_view_rect(windowsize))
            self.on_resize()
        
        
    def get_view_rect(self, windowsize):
        """Return the rect of the main view for this screen."""
        return 0, 0, 0, 0
    
    
    def on_resize(self):
        """A hook that runs whenever the view is resized."""
        pass


        