import pygame
from pygame.locals import *


class Game:
    move_keys = K_UP, K_RIGHT, K_DOWN, K_LEFT
        
    def __init__(self, level, tilepath, tilesize):
        self.level = level
        
        # init sprite tileset
        self.tileimg = pygame.image.load(tilepath)
        self.tiledims = self.tileimg.get_width() / tilesize, self.tileimg.get_height() / tilesize
        
        # init view
        self.viewsize = 10, 6
        self.set_viewsize(pygame.display.get_surface().get_size())
        
        # draw the initial frame
        self.draw_frame()
            
            
    def set_viewsize(self, (ww, wh)):
        """Set the cell size, and thus the view size, so that the view
        fits within the window."""
        # init screen of proper size within the window
        self.windowsize = ww, wh
        vw, vh = self.viewsize
        self.cellsize = min(ww / vw, wh / vh)
        self.width, self.height = vw * self.cellsize, vh * self.cellsize
        self.left, self.top = int((ww - self.width) / 2), int((wh - self.height) / 2)
        self.view = pygame.display.get_surface().subsurface((self.left, self.top, self.width, self.height))

        # init tileset
        tilew, tileh = self.tiledims
        self.tileset = pygame.transform.scale(self.tileimg.convert_alpha(),
                                              (tilew * self.cellsize, tileh * self.cellsize))
        
        self.level.redraw = True
        
        
    def run_frame(self, elapsed, keys):
        """Run a single frame for this level."""
        status = 'ok',
        
        # check collisions
        for sprite in self.level.sprites:
            sprite.check_collisions()

        # check for death
        if not self.level.player.alive():
            status = 'dead', 0
        if any(not rover.alive() for rover in self.level.get_sprites('Rover')):
            status = 'dead', 1
        
        # check for win condition
        if self.level.player.done_level():
            status = 'win',

        # handle events
        for key, keydown in keys:
            
            # move controls
            if keydown and key in self.move_keys:
                self.level.player.move_key_down(self.move_keys.index(key))
                    
            elif not keydown and key in self.move_keys:
                self.level.player.move_key_up(self.move_keys.index(key))
            
            # skip level
            elif keydown and key == K_RETURN:
                status = 'win',
                
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
        self.draw_frame()
        
        return status


    def draw_frame(self):
        """Draw a frame at the current state of the level."""
        # check for window resize
        windowsize = pygame.display.get_surface().get_size()
        if self.windowsize != windowsize:
            self.set_viewsize(windowsize)
        
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
        vw, vh = self.viewsize
        ox = px - (vw - 1) / 2.0
        oy = py - (vh - 1) / 2.0
        
        # clamp values so as not to go off the edge
        ox = max(0, min(ox, self.level.width - vw))
        oy = max(0, min(oy, self.level.height - vh))

        # blit background onto the view
        left, top = int(ox * self.cellsize), int(oy * self.cellsize)
        self.view.blit(self.background, (0, 0), (left, top, self.width, self.height))

        # update sprite positions, draw sprites, update display
        self.level.sprites.update(self.cellsize, (left, top), self.tileset)
        self.level.sprites.draw(self.view)
        pygame.display.update()
        
        

