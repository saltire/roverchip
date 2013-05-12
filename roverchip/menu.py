import os

import pygame

import config
from font import Font
from game import Game
from screen import Screen


class Menu(Screen):
    def __init__(self, window):
        self.font = Font(config.menufontpath, config.menufontsize)

        # init menu display
        self.selected = 0
        self.col_offset = 0
        
        Screen.__init__(self, window)
        
        
    def resize_view(self, size):
        """Resize the view, redraw the background, reinit the font."""
        # find the largest rectangle with the same ratio as basesize,
        # and a maximum of maxsize on either axis.
        ww, wh = size
        bw, bh = config.menuratio
        mx, my = config.menumargin
        mult = min(ww * (1 - mx * 2) / bw, wh * (1 - my * 2) / bh)
        width, height = bw * mult, bh * mult
        left, top = (ww - width) / 2, (wh - height) / 2
        self.view = self.window.view.subsurface((left, top, width, height))
        
        # redraw the background
        self.background = pygame.Surface(self.view.get_size())
        self.background.fill(config.menubackcolor)
        
        # create text area
        tmx, tmy = config.menumargin
        tleft, ttop = tmx * width, tmy * height
        twidth, theight = width - tleft * 2, height - ttop * 2
        self.textarea = self.view.subsurface((tleft, ttop, twidth, theight))
        
        # find biggest font size that will fit the max number of rows
        # with the given leading, without going under the min size
        for size in range(config.maxfontsize, config.minfontsize - 1, -config.sizestep):
            rowtotal = size * config.maxrows
            leadtotal = int(size * config.leadpct) * (config.maxrows - 1)
            if rowtotal + leadtotal <= self.textarea.get_height():
                rows = config.maxrows
                break
            
            # if no size in range fits, start reducing number of rows
            if size == config.minfontsize:
                for rows in range(config.maxrows - 1, 0, -1):
                    rowtotal = size * rows
                    if rowtotal + leadtotal <= self.textarea.get_height():
                        break
        
        self.fsize = size
        self.rows = rows
        self.leading = int(size * config.leadpct)
        
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
            
            columns = config.columns
            colwidth = self.textarea.get_width() / columns
            
            srow = self.selected % self.rows
            scol = self.selected / self.rows
            
            # adjust offset to within (columns) of col
            self.col_offset = min(scol, max(self.col_offset, scol - columns + 1))
            
            # render and blit each line of text in each column that is showing
            options = self.options[self.rows * self.col_offset:
                                   self.rows * (self.col_offset + columns)]
            optfonts = self.font.render([option[0] for option in options],
                                        self.fsize, color=config.menufontcolor)
            
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
                    
            # enter key: open selected screen or quit this menu
            elif keydown and key == pygame.K_RETURN:
                screen, args = self.options[self.selected][1:]
                
                if not screen:
                    return False
                
                self.selected = 0
                self.redraw = True
                return screen(self.window, *args)
            
            # escape key: quit menu
            elif keydown and key == pygame.K_ESCAPE:
                return False
                


class MainMenu(Menu):
    def __init__(self, window, leveldata):
        self.options = [('Play Game', LevelSelect, [leveldata]),
                        ('Quit Game', False, ()),
                        ]
        Menu.__init__(self, window)



class LevelSelect(Menu):
    def __init__(self, window, leveldata):
        self.options = [('Level ' + str(i + 1), Game, [leveldata, i])
                        for i in range(len(leveldata))]
        Menu.__init__(self, window)

        