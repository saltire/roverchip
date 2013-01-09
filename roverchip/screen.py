class Screen:
    def __init__(self, window):
        """Draws the initial frame. Make sure to initialize any variables needed
        to draw before calling this method from a subclass."""
        self.window = window
        self.last_windowsize = None
        
        
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


        