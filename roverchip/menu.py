import os

import pygame

from font import Font
from game import Game
from screen import Screen


class Menu(Screen):
    def __init__(self, window):
        # text properties
        fontpath = window.config.get('fontpath')
        fontsize = window.config.getints('fontsize')
        self.font = Font(os.path.join(window.path, fontpath), fontsize)
        self.fontcolor = window.config.getints('menufontcolor')

        # init menu display
        self.selected = 0
        self.col_offset = 0
        
        Screen.__init__(self, window)
        
        
    def resize_view(self, size):
        """Resize the view, redraw the background, reinit the font."""
        # find the largest rectangle with the same ratio as basesize,
        # and a maximum of maxsize on either axis.
        ww, wh = size
        bw, bh = self.window.config.getints('menuratio')
        mx, my = self.window.config.getfloats('menumargin')
        mult = min(ww * (1 - mx * 2) / bw, wh * (1 - my * 2) / bh)
        width, height = bw * mult, bh * mult
        left, top = (ww - width) / 2, (wh - height) / 2
        self.view = self.window.view.subsurface((left, top, width, height))
        
        # redraw the background
        self.background = pygame.Surface(self.view.get_size())
        self.background.fill(self.window.config.getints('menubackcolor'))
        
        # create text area
        tmx, tmy = self.window.config.getfloats('textmargin')
        tleft, ttop = tmx * width, tmy * height
        twidth, theight = width - tleft * 2, height - ttop * 2
        self.textarea = self.view.subsurface((tleft, ttop, twidth, theight))
        
        # find biggest font size that will fit the max number of rows
        # with the given leading, without going under the min size
        maxrows = self.window.config.getint('maxrows')
        maxsize = self.window.config.getint('maxfontsize')
        minsize = self.window.config.getint('minfontsize')
        sizestep = self.window.config.getint('sizestep')
        leadpct = self.window.config.getfloat('leadpct')
        for size in range(maxsize, minsize - 1, -sizestep):
            rowtotal = size * maxrows
            leadtotal = int(size * leadpct) * (maxrows - 1)
            if rowtotal + leadtotal <= self.textarea.get_height():
                rows = maxrows
                break
            
            # if no size in range fits, start reducing number of rows
            if size == minsize:
                for rows in range(maxrows - 1, 0, -1):
                    rowtotal = size * rows
                    if rowtotal + leadtotal <= self.textarea.get_height():
                        break
        
        self.fsize = size
        self.rows = rows
        self.leading = int(size * leadpct)
        
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
            
            columns = self.window.config.getint('columns')
            colwidth = self.textarea.get_width() / columns
            
            srow = self.selected % self.rows
            scol = self.selected / self.rows
            
            # adjust offset to within (columns) of col
            self.col_offset = min(scol, max(self.col_offset, scol - columns + 1))
            
            # render and blit each line of text in each column that is showing
            options = self.options[self.rows * self.col_offset:
                                   self.rows * (self.col_offset + columns)]
            optfonts = self.font.render([option[0] for option in options],
                                        self.fsize, color=self.fontcolor)
            
            for i, optfont in enumerate(optfonts):
                pos = (i / self.rows * colwidth + self.fsize,
                       i % self.rows * (self.fsize + self.leading))
                self.textarea.blit(optfont, pos)
            
            # blit marker
            mmargin = self.fsize / 4
            self.textarea.blit(self.marker, ((scol - self.col_offset) * colwidth + mmargin,
                                             srow * (self.fsize + self.leading) + mmargin))
            
            self.redraw = False


    def run_frame(self, elapsed, keys):
        """Scan for keystrokes and either switch menus or take actions."""
        for key, keydown in keys:
            # arrow keys: change selection
            if keydown and key in (pygame.K_UP, pygame.K_RIGHT,
                                   pygame.K_DOWN, pygame.K_LEFT):
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
                screen, args = self.options[self.selected][1:]
                
                if not screen:
                    return 'quit'
                
                print screen, len(args)
                self.window.run(screen(self.window, *args))
                self.selected = 0
                self.redraw = True
            
            # escape key: quit menu
            elif keydown and key == pygame.K_ESCAPE:
                return 'quit'
                


class MainMenu(Menu):
    def __init__(self, window, leveldata):
        self.options = [('Play Game', LevelSelect, (leveldata,)),
                        ('Quit Game', False, ()),
                        ]
        Menu.__init__(self, window)



class LevelSelect(Menu):
    def __init__(self, window, leveldata):
        self.options = [('Level ' + str(i + 1), Game, (leveldata, i))
                        for i in range(len(leveldata))]
        Menu.__init__(self, window)

        