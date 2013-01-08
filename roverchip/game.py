import os

import pygame

from level import Level
from screen import Screen


class Game(Screen):
    move_keys = pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT
        
    def __init__(self, window, leveldata, lskip=0, tilepath='tiles.png', tilesize=16):
        self.viewcells = 10, 6  # size of the view in cells
        
        # init levels
        self.leveldata = leveldata
        self.current_level = lskip
        self.level = Level(*self.leveldata[self.current_level])
        
        # init sprite tileset
        self.tileimg = pygame.image.load(os.path.join(window.path, tilepath))
        self.tiledims = self.tileimg.get_width() / tilesize, self.tileimg.get_height() / tilesize
        
        Screen.__init__(self, window)
        
        
    def find_view_rect(self, windowsize):
        """Set the cell size to create the largest possible rectangle with
        the same ratio as viewcells."""
        # init view of proper size within the window
        ww, wh = windowsize
        vw, vh = self.viewcells
        self.cellsize = min(ww / vw, wh / vh)        
        width, height = vw * self.cellsize, vh * self.cellsize
        left, top = int((ww - width) / 2), int((wh - height) / 2)
        
        return left, top, width, height
        
        
    def on_resize(self):
        """Resize the tileset, and redraw the entire level."""
        # init tileset
        tilew, tileh = self.tiledims
        self.tileset = pygame.transform.scale(self.tileimg.convert_alpha(),
                                              (tilew * self.cellsize, tileh * self.cellsize))
        self.level.redraw = True
        
        
    def run_frame(self, elapsed, keys):
        """Run a single frame for this level."""
        # check collisions
        for sprite in self.level.sprites:
            sprite.check_collisions()

        # check for death -> reset level
        if (not self.level.player.alive()
            or any(not rover.alive() for rover in self.level.get_sprites('Rover'))):
            self.level = Level(*self.leveldata[self.current_level])
        
        # check for win condition -> advance level, or quit if last level
        if self.level.player.done_level():
            if self._advance_level() is False:
                return 'quit'

        # handle events
        for key, keydown in keys:
            # move controls
            if keydown and key in self.move_keys:
                self.level.player.move_key_down(self.move_keys.index(key))
                    
            elif not keydown and key in self.move_keys:
                self.level.player.move_key_up(self.move_keys.index(key))
            
            # skip level, or quit if last level
            elif keydown and key == pygame.K_RETURN:
                if self._advance_level() is False:
                    return 'quit'
                
        # run hooks for all sprites in layer order
        for sprite in self.level.sprites:
            sprite.start_turn()
            
        for sprite in self.level.sprites:
            sprite.do_move(elapsed)
            
        for sprite in self.level.sprites:
            if sprite.new_cell:
                sprite.after_move()
                sprite.new_cell = False
                
        for sprite in self.level.sprites:
            sprite.end_turn()


    def _advance_level(self):
        """Get the next level, or return False if there is no next level."""
        try:
            self.current_level += 1
            self.level = Level(*self.leveldata[self.current_level])
            
        except IndexError:
            return False
        
        
    def draw_frame(self):
        """Draw a frame at the current state of the level."""
        # redraw cells
        if self.level.redraw:
            # draw entire level background
            self.background = pygame.Surface((self.level.width * self.cellsize, self.level.height * self.cellsize))
            redraw_cells = self.level.cells.keys()
            self.level.redraw = False
        else:
            # draw individual cells
            redraw_cells = self.level.redraw_cells.copy()
            self.level.redraw_cells.clear()
            
        for cx, cy in redraw_cells:
            self.background.blit(self.level.get_cell((cx, cy)).draw(self.cellsize, self.tileset),
                                 (cx * self.cellsize, cy * self.cellsize))
                
        # find offset that places the player in the centre
        px, py = self.level.player.pos
        vw, vh = self.viewcells
        ox = px - (vw - 1) / 2.0
        oy = py - (vh - 1) / 2.0
        
        # clamp values so as not to go off the edge
        ox = max(0, min(ox, self.level.width - vw))
        oy = max(0, min(oy, self.level.height - vh))

        # blit background onto the view
        left, top = int(ox * self.cellsize), int(oy * self.cellsize)
        width, height = self.view.get_size()
        self.view.blit(self.background, (0, 0), (left, top, width, height))

        # update sprite positions, draw sprites, update display
        self.level.sprites.update(self.cellsize, (left, top), self.tileset)
        self.level.sprites.draw(self.view)
        
        
