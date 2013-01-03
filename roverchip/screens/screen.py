import pygame


class Screen:
    def __init__(self):
        self.windowsize = None
    
    
    def _init_view(self):
        """If window size has changed, set the cell size and reinitialize
        the view so that it fits within the window."""
        # check if the window size has changed
        windowsize = pygame.display.get_surface().get_size()
        if self.windowsize == windowsize:
            return False
        self.windowsize = windowsize
        
        self.view = pygame.display.get_surface().subsurface(self._get_view_rect())


    def run_frame(self, elapsed, keys):
        """Run a single frame for this screen."""
        pass
        