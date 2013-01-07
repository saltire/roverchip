import pygame


class Screen:
    def __init__(self):
        self.windowsize = None

        # draw the initial frame
        self.draw_frame()
    
    
    def resize_view(self):
        """Runs once per frame. If window size has changed, reinitialize
        the view and any elements within that need to be resized."""
        # check if the window size has changed
        windowsize = pygame.display.get_surface().get_size()
        if self.windowsize == windowsize:
            return False
        
        self.windowsize = windowsize
        
        # initialize view using rect from child class
        self.view = pygame.display.get_surface().subsurface(self.find_view_rect())
        
        return True
        
        
    def get_view_rect(self):
        """Return the rect of the main view for this screen."""
        return 0, 0, 0, 0


    def run_frame(self, elapsed, keys):
        """Run a single frame for this screen."""
        pass
        