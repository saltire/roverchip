import pygame
from pygame.locals import *


class Game:
    move_keys = K_UP, K_RIGHT, K_DOWN, K_LEFT
        
    def __init__(self, levels, lskip=0, tilepath='tiles.png', tilesize=16):
        # init levels
        self.levels = (level for level in levels[lskip:])
        self.level = next(self.levels)
        
        # init sprite tileset
        self.tileimg = pygame.image.load(tilepath)
        self.tiledims = self.tileimg.get_width() / tilesize, self.tileimg.get_height() / tilesize
        
        # init view
        self.viewcells = 10, 6
        self.windowsize = None
        self._set_viewsize()
        
        # draw the initial frame
        self._draw_frame()
        
        
    def _set_viewsize(self):
        """If window size has changed, set the cell size and reinitialize
        the view so that it fits within the window."""
        # check if the window size has changed
        ww, wh = pygame.display.get_surface().get_size()
        if self.windowsize == (ww, wh):
            return
        self.windowsize = ww, wh
        
        # init view of proper size within the window
        vw, vh = self.viewcells
        self.cellsize = min(ww / vw, wh / vh)        
        width, height = vw * self.cellsize, vh * self.cellsize
        left, top = int((ww - width) / 2), int((wh - height) / 2)
        self.view = pygame.display.get_surface().subsurface((left, top, width, height))

        # init tileset
        tilew, tileh = self.tiledims
        self.tileset = pygame.transform.scale(self.tileimg.convert_alpha(),
                                              (tilew * self.cellsize, tileh * self.cellsize))
        
        self.level.redraw = True
        
        
    def run_frame(self, elapsed, keys):
        """Run a single frame for this level."""
        self.status = 'ok',
        
        # check collisions
        for sprite in self.level.sprites:
            sprite.check_collisions()

        # check for death
        if not self.level.player.alive():
            self.status = 'dead', 0
        if any(not rover.alive() for rover in self.level.get_sprites('Rover')):
            self.status = 'dead', 1
        
        # check for win condition
        if self.level.player.done_level():
            self.status = self._advance_level()

        # handle events
        for key, keydown in keys:
            
            # move controls
            if keydown and key in self.move_keys:
                self.level.player.move_key_down(self.move_keys.index(key))
                    
            elif not keydown and key in self.move_keys:
                self.level.player.move_key_up(self.move_keys.index(key))
            
            # skip level
            elif keydown and key == K_RETURN:
                self.status = self._advance_level()
                
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
            
        # draw the frame again
        self._draw_frame()
        
        return self.status


    def _advance_level(self):
        """Get the next level, or return False if there is no next level."""
        try:
            self.level = next(self.levels)
            return self.status
        
        except StopIteration:
            return 'win',
        
        
    def _draw_frame(self):
        """Draw a frame at the current state of the level."""
        # check for window resize
        self._set_viewsize()
        
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
        pygame.display.update()
        
        

