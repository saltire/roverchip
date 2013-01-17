import os

import pygame

from font import Font
from game import Game
from screen import Screen


class Menu(Screen):
    arrow_keys = pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT

    def __init__(self, window, levels, fontpath='font.png', fontsize=(8, 8)):
        # subwindow properties
        self.backcolor = 255, 255, 255
        self.basesize = 3, 2
        self.margin = 0.05, 0.05
        self.textmargin = 0.05, 0.1
        
        # text properties
        self.font = Font(os.path.join(window.path, fontpath), fontsize)
        self.color = 0, 0, 0
        self.maxrows = 8
        self.maxsize = 96
        self.minsize = 32
        self.cols = 2
        self.kernpct = 0.125
        self.leadpct = 0.4
        
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
        self.background.fill(self.backcolor)
        
        # create text area
        tmx, tmy = self.textmargin
        tleft, ttop = tmx * width, tmy * height
        twidth, theight = width - tleft * 2, height - ttop * 2
        self.textarea = self.view.subsurface((tleft, ttop, twidth, theight))
        
        # find biggest font size that will fit the max number of rows
        # with the given leading, without going under the min size
        for size in range(self.maxsize, self.minsize - 1, -1):
            rowtotal = size * self.maxrows
            leadtotal = int(size * self.leadpct) * (self.maxrows - 1)
            if rowtotal + leadtotal < self.textarea.get_height():
                break
        self.fsize = size
        self.leading = int(size * self.leadpct)
        self.kerning = int(size * self.kernpct)
        
        # reduce the number of rows if font is at min size
        # and max rows still don't fit
        self.rows = next(num for num in range(self.maxrows, 0, -1)
                         if num * self.fsize < self.textarea.get_height()
                         or num == 1)

        # draw marker
        msize = self.fsize / 2
        self.marker = pygame.Surface((msize, msize))
        self.marker.fill((255, 0, 0))

        self.redraw = True


    def draw_frame(self):
        """Draw the visible columns of options on the screen, and the marker."""
        if self.redraw:
            # blit the background, text and marker onto the view
            self.view.blit(self.background, (0, 0))
            
            colwidth = self.textarea.get_width() / self.cols
            
            srow = self.selected % self.rows
            scol = self.selected / self.rows
            
            # adjust offset to within (self.cols) of col
            self.col_offset = min(scol, max(self.col_offset, scol - self.cols + 1))
            
            # render and blit each column of text that is showing
            for col in range(self.col_offset, self.col_offset + self.cols):
                options = self.options[col * self.rows:(col + 1) * self.rows]
                if not options:
                    break
                
                colfont = self.font.render('\n'.join(text for _, text in options),
                                           self.fsize, self.leading, self.kerning, self.color)
                self.textarea.blit(colfont, ((col - self.col_offset) * colwidth + self.fsize, 0))
            
            # blit marker
            mmargin = self.fsize / 4
            self.textarea.blit(self.marker, ((scol - self.col_offset) * colwidth + mmargin,
                                             srow * (self.fsize + self.leading) + mmargin))
            
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
                
