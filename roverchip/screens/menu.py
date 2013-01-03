from screen import Screen


class Menu(Screen):
    def __init__(self):
        Screen.__init__(self)
    
        self.basesize = 3, 2
        self.maxsize = .75, .75
        
    
    def _get_view_rect(self):
        """Create the largest rectangle of the same ratio as basesize, with
        a maximum of maxsize on both axes."""
        ww, wh = self.windowsize
        bw, bh = self.basesize
        mw, mh = self.maxsize
        mult = min(ww * mw / bw, wh * mh / bh)
        width, height = bw * mult, bh * mult
        left, top = (ww - width) / 2, (wh - height) / 2
        
        return left, top, width, height


    def run_frame(self, elapsed, keys):
        self._init_view()
        self.view.fill((255, 255, 255))
        return 'ok',