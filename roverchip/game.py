import pygame

import config
from level import Level
from screen import Screen
from tileset import Tileset


class Game(Screen):
    move_keys = pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT
        
    def __init__(self, leveldata, lskip=0):
        self.viewcells = 10, 6  # size of the view in cells
        
        # init levels
        self.leveldata = leveldata
        self.current_level = lskip
        self.level = Level(self.leveldata[self.current_level])
        
        self.tileset = Tileset(config.tilepath, config.tilesize)
        
        
    def resize_view(self):
        """Set cell size, and resize the view and the tileset."""
        # find the largest rectangle with the same ratio as viewcells
        ww, wh = self.window_view.get_size()
        vw, vh = self.viewcells
        self.cellsize = min(ww / vw, wh / vh)        
        width, height = vw * self.cellsize, vh * self.cellsize
        left, top = int((ww - width) / 2), int((wh - height) / 2)
        self.view = self.window_view.subsurface((left, top, width, height))
        
        self.tileset.init_tileset(self.cellsize)

        self.level.redraw = True
        
        
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
        
        
    def run_frame(self, elapsed, keys):
        """Run a single frame for this level."""
        def advance_level():
            # start the next level, or return false if there is none
            self.current_level += 1
            try:
                self.level = Level(self.leveldata[self.current_level])
            except IndexError:
                return False
        
        # check collisions
        for sprite in self.level.sprites:
            sprite.check_collisions()

        # check for death -> reset level
        if self.level.check_for_failure():
            self.level = Level(self.leveldata[self.current_level])
        
        # check for win condition -> advance level, or quit if last level
        if self.level.check_for_success():
            if advance_level() is False:
                return False

        # handle events
        for key, keydown in keys:
            # move controls
            if keydown and key in self.move_keys:
                self.level.player.move_key_down(self.move_keys.index(key))
                    
            elif not keydown and key in self.move_keys:
                self.level.player.move_key_up(self.move_keys.index(key))
            
            # skip level, or quit if last level
            elif keydown and key == pygame.K_RETURN:
                if advance_level() is False:
                    return False
            
            # quit to menu
            elif keydown and key == pygame.K_ESCAPE:
                return False
                
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

