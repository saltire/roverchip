import pygame

from game import Game
from screen import Screen


class Menu(Screen):
    arrow_keys = pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT

    def __init__(self, window, levels):
        # subwindow properties
        self.basesize = 3, 2
        self.margin = 0.05, 0.05
        self.textmargin = 0.05, 0.1
        
        # text properties
        self.maxrows = 8
        self.maxsize = 100
        self.minsize = 30
        self.cols = 2
        
        # init menu options
        self.menu = 'main'
        self.mainmenu = [('play', 'Play Game'),
                        ('quit', 'Quit Game'),
                        ]
        self.options = self.mainmenu
        self.selected = 0
        self.col_offset = 0
        
        # init levels
        self.levels = levels
        
        Screen.__init__(self, window)
        
        
    def resize_view(self, size):
        """Resize the view, redraw the background, reinit the font."""
        # find the largest rectangle with the same ratio as basesize,
        # and a maximum of maxsize on either axis.
        ww, wh = size
        bw, bh = self.basesize
        mx, my = self.margin
        mult = min(ww * (1 - mx * 2) / bw, wh * (1 - my * 2) / bh)
        width, height = bw * mult, bh * mult
        left, top = (ww - width) / 2, (wh - height) / 2
        self.view = self.window.view.subsurface((left, top, width, height))
        
        # redraw the background
        self.background = pygame.Surface(self.view.get_size())
        self.background.fill((255, 255, 255))
        
        # create text area
        tmx, tmy = self.textmargin
        tleft, ttop = tmx * width, tmy * height
        twidth, theight = width - tleft * 2, height - ttop * 2
        self.textarea = self.view.subsurface((tleft, ttop, twidth, theight))
        
        # find biggest font size that will fit the max number of rows
        # but without going under the min size
        self.rheight = next(size for size in range(self.maxsize, self.minsize - 1, -1)
                        if size * self.maxrows < self.textarea.get_height()
                        or size == self.minsize)
        self.font = pygame.font.Font(None, self.rheight)
        
        # reduce the number of rows if font is at min size
        # and max rows still don't fit
        self.rows = next(num for num in range(self.maxrows, 0, -1)
                         if num * self.rheight < self.textarea.get_height()
                         or num == 1)

        # draw marker
        msize = self.font.get_height() / 2
        self.marker = pygame.Surface((msize, msize))
        self.marker.fill((255, 0, 0))

        self.redraw = True


    def draw_frame(self):
        """Draw the visible columns of options on the screen, and the marker."""
        if self.redraw:
            # blit the background, text and marker onto the view
            self.view.blit(self.background, (0, 0))
            
            fheight = self.font.get_height()
            colwidth = self.textarea.get_width() / self.cols
            
            row = self.selected % self.rows
            col = self.selected / self.rows
            # adjust offset to within (self.cols) of col
            self.col_offset = min(col, max(self.col_offset, col - self.cols + 1))
            options = self.options[self.col_offset * self.rows:
                                   (self.col_offset + self.cols) * self.rows]
            
            for i, (_, text) in enumerate(options):
                # blit text onto its row, indenting by fheight
                self.textarea.blit(self.font.render(text, True, (0, 0, 0)),
                                   (i / self.rows * colwidth + fheight,
                                    i % self.rows * self.rheight))
            
            # blit marker
            mmargin = self.font.get_height() / 4
            self.textarea.blit(self.marker, ((col - self.col_offset) * colwidth + mmargin,
                                             row * self.rheight + mmargin))
            
            self.redraw = False


    def run_frame(self, elapsed, keys):
        """Scan for keystrokes and either switch menus or take actions."""
        for key, keydown in keys:
            # arrow keys: change selection
            if keydown and key in self.arrow_keys:
                col = self.selected / self.rows
                totalcols = (len(self.options) + self.rows - 1) / self.rows
                old_selected = self.selected

                if key in (pygame.K_UP, pygame.K_DOWN):
                    # move marker up or down
                    mod = 1 if key == pygame.K_DOWN else -1
                    self.selected = max(0, min(self.selected + mod, len(self.options) - 1))
                    
                elif key == pygame.K_LEFT and col > 0:
                    # move marker left
                    self.selected -= self.rows
                    
                elif key == pygame.K_RIGHT and col < totalcols - 1:
                    # move marker right
                    self.selected = min(self.selected + self.rows,
                                        len(self.options) - 1)
                    
                if self.selected != old_selected:
                    self.redraw = True
                    
            # enter key: act on selection value
            elif keydown and key == pygame.K_RETURN:
                value = self.options[self.selected][0]
                
                if self.menu == 'main':
                    if value == 'play':
                        self.menu = 'levels'
                        self.options = [(i, 'Level ' + str(i + 1))
                                        for i in range(len(self.levels))]
                        self.selected = 0
                        self.redraw = True
                        
                    elif value == 'quit':
                        return 'quit'
                
                elif self.menu == 'levels':
                    # start the game screen, skipping to the selected level
                    self.window.run(Game(self.window, self.levels, value))
                    self.menu = 'main'
                    self.options = self.mainmenu
                    self.selected = 0
                    self.redraw = True
            
            # escape key: quit menu
            elif keydown and key == pygame.K_ESCAPE:
                if self.menu == 'main':
                    print 'quitting'
                    return 'quit'
                
                elif self.menu == 'levels':
                    print 'yikes'
                    self.menu = 'main'
                    self.options = self.mainmenu
                    self.selected = 0
                    self.redraw = True
                
