class Screen:
    def __init__(self, window):
        """Draws the initial frame. Make sure to initialize any variables needed
        to draw before calling this method from a subclass."""
        self.window = window
        self.resize_view(window.view.get_size())
        
        
    def resize_view(self):
        """A hook that runs whenever the view is resized."""
        pass

    
    def draw_frame(self):
        """Render any visible changes to the frame."""
        pass


    def run_frame(self, elapsed, keys):
        """Process any input and take any actions for one frame,
        and optionally return a status."""
        pass
