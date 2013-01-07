import pygame

from screen import Screen


class Menu(Screen):
    def __init__(self):
        self.basesize = 3, 2
        self.maxsize = .9, .9
        
        self.fontheight = 50
        self.options = [('play', 'Play Game'),
                        ('quit', 'Quit Game'),
                        ]

        self.selected = 0
        self.marker = pygame.surface.Surface((20, 20))
        self.marker.fill((255, 0, 0))
        self.arrow_timeout = 0

        Screen.__init__(self)
        
        
    def find_view_rect(self):
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
        status = 'ok',
        
        if self.arrow_timeout > 0:
            self.arrow_timeout -= elapsed
        
        for key, keydown in keys:
            # move marker up or down
            if (keydown and key in (pygame.K_UP, pygame.K_DOWN)
                and self.arrow_timeout <= 0):
                mod = 1 if key == pygame.K_DOWN else -1
                self.selected = (self.selected + mod) % len(self.options)
                self.arrow_timeout = 100
                self.redraw = True
                
            # return selection on hitting enter
            elif keydown and key == pygame.K_RETURN:
                status = self.options[self.selected][0],
        
        # draw the frame again
        self.draw_frame()
        
        return status
    
    
    def draw_frame(self):
        if self.resize_view():
            # redraw the background and render the text
            self.background = pygame.surface.Surface(self.view.get_size())
            self.background.fill((255, 255, 255))
    
            left, top = 50, 50
            font = pygame.font.Font(None, self.fontheight)
            for i, (_, text) in enumerate(self.options):
                self.background.blit(font.render(text, True, (0, 0, 0)),
                                     (left, top + self.fontheight * i))
            self.redraw = True

        if self.redraw:
            # blit the background and the marker onto the view
            left, top = 15, 55
            self.view.blit(self.background, (0, 0))
            self.view.blit(self.marker, (left, top + self.fontheight * self.selected))
            self.redraw = False

