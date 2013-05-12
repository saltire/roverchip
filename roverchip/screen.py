class Screen:
    def __init__(self):
        pass
        
        
    def set_view(self, view):
        """Store the window's view, from which to create subsurfaces. Then
        call the resize view hook."""
        self.window_view = view
        self.resize_view()
        
        
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
