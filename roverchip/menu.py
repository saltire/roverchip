import pygame

from game import Game
from screen import Screen


class Menu(Screen):
    def __init__(self, window, levels):
        # init subwindow
        self.basesize = 3, 2
        self.maxsize = .9, .9
        
        # init menu options
        self.fontheight = 50
        self.mainmenu = [('play', 'Play Game'),
                        ('quit', 'Quit Game'),
                        ]
        self.options = self.mainmenu

        # init marker
        self.selected = 0
        self.marker = pygame.surface.Surface((20, 20))
        self.marker.fill((255, 0, 0))
        self.arrow_timeout = 0
        
        # init levels
        self.levels = levels
        
        Screen.__init__(self, window)
        
        
    def find_view_rect(self, windowsize):
        """Create the largest rectangle of the same ratio as basesize, with
        a maximum of maxsize on both axes."""
        ww, wh = windowsize
        bw, bh = self.basesize
        mw, mh = self.maxsize
        mult = min(ww * mw / bw, wh * mh / bh)
        width, height = bw * mult, bh * mult
        left, top = (ww - width) / 2, (wh - height) / 2
        
        return left, top, width, height
    
    
    def on_resize(self):
        # redraw the background
        self.background = pygame.Surface(self.view.get_size())
        self.background.fill((255, 255, 255))
        
        self.redraw = True


    def run_frame(self, elapsed, keys):
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
                action = self.options[self.selected][0]
                
                if action == 'play':
                    self.options = ([(i, 'Level ' + str(i + 1))
                                     for i in range(len(self.levels))]
                                    + [('back', 'Back')])
                    self.selected = 0
                    self.redraw = True
                    
                elif action == 'quit':
                    return 'quit'
                
                elif action == 'back':
                    self.options = self.mainmenu
                    self.selected = 0
                    self.redraw = True
                    
                else:
                    # start the game screen, skipping to the selected level
                    self.window.run(Game(self.window, self.levels, action))
                    self.options = self.mainmenu
                    self.selected = 0
                    self.redraw = True
            
    
    def draw_frame(self):
        if self.redraw:
            # blit the background, text and marker onto the view
            self.view.blit(self.background, (0, 0))
            
            maxsize = 50
            minsize = 20
            fontsize = next(size for size in range(maxsize, minsize - 1, -1)
                            if size * len(self.options) < self.view.get_height()
                            or size == minsize)
            
            left, top = 50, 0
            font = pygame.font.Font(None, fontsize)
            for i, (_, text) in enumerate(self.options):
                self.view.blit(font.render(text, True, (0, 0, 0)),
                                     (left, top + fontsize * i))
            left, top = 15, 5
            self.view.blit(self.marker, (left, top + fontsize * self.selected))
            
            self.redraw = False

