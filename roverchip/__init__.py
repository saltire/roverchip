import sys

import pygame
from pygame.locals import *

import levelfile


class Roverchip:
    def __init__(self, levelpath, tilepath, tilesize):
        pygame.init()
        
        # init clock
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick()

        # init keyboard settings
        pygame.key.set_repeat(1, 50)

        # init sprite tileset
        self.tileimg = pygame.image.load(tilepath)
        self.tiledims = self.tileimg.get_width() / tilesize, self.tileimg.get_height() / tilesize
        
        # init window
        cellsize = 80
        self.viewsize = 10, 6
        vw, vh = self.viewsize
        self.init_window((vw * cellsize, vh * cellsize))
        
        # start loop
        # init map
        for level in levelfile.LevelFile(levelpath).get_levels():
            self.loop(level)
            
        sys.exit('Yay!')
        
        
    def init_window(self, (width, height)):
        """Initialize the game window. Called at beginning, and every time
        the window is resized."""
        # init window and background
        self.window = pygame.display.set_mode((width, height), RESIZABLE)
        self.window.fill((0, 0, 0))
        
        # init screen of proper size within the window
        vw, vh = self.viewsize
        self.cellsize = min(width / vw, height / vh)
        self.width, self.height = vw * self.cellsize, vh * self.cellsize
        self.left, self.top = int((width - self.width) / 2), int((height - self.height) / 2)
        self.view = self.window.subsurface((self.left, self.top, self.width, self.height))

        # init tileset
        tilew, tileh = self.tiledims
        self.tileset = pygame.transform.scale(self.tileimg.convert_alpha(),
                                                    (tilew * self.cellsize, tileh * self.cellsize))
        

    def draw_level(self, level):
        """Initialize the level background and the current position of sprites.
        Called when new levels are loaded, and after resizing."""
        # init background
        self.background = pygame.Surface((level.width * self.cellsize, level.height * self.cellsize))
        
        tiles = {}
        for cx, cy in level.cells:
            cell = level.get_cell((cx, cy))
            tx, ty = cell.tile
            tilerect = [i * self.cellsize for i in (tx, ty, 1, 1)]
            tileimg = tiles.setdefault(cell.tile, self.tileset.subsurface(tilerect))
            if cell.rotate != 0:
                tileimg = pygame.transform.rotate(tileimg, cell.rotate * -90)
            self.background.blit(tileimg, (cx * self.cellsize, cy * self.cellsize))
            
        # draw background
        left, top = self.find_offset(level)
        self.view.blit(self.background, (0, 0), (left, top, self.width, self.height))

        # draw sprites
        level.sprites.update(self.cellsize, (left, top), self.tileset)
        level.sprites.draw(self.view)

        # update display
        pygame.display.update()
        
        
    def find_offset(self, level):
        """Return the top and left offset of the view relative to the
        entire area of the level."""
        px, py = level.player.pos
        vw, vh = self.viewsize
        
        # find offset that places the player in the centre
        ox = px - (vw - 1) / 2.0
        oy = py - (vh - 1) / 2.0
        
        # clamp values so as not to go off the edge
        left = max(0, min(ox, level.width - vw))
        top = max(0, min(oy, level.height - vh))
        
        return int(left * self.cellsize), int(top * self.cellsize)

        
    def loop(self, level):
        """The event loop for the running level."""
        dirkeys = K_UP, K_RIGHT, K_DOWN, K_LEFT
        
        self.draw_level(level)
        
        while True:
            # update clock
            old_time = self.time
            self.time += self.clock.tick()
            elapsed = min((self.time - old_time) / 1000.0, 0.015)
            
            # handle events
            for event in pygame.event.get():
                
                # close window
                if event.type == QUIT:
                    sys.exit()
                
                # resize window
                elif event.type == VIDEORESIZE:
                    self.init_window(event.size)
                    self.draw_level(level)
                    
                # move controls
                elif event.type == KEYDOWN:
                    if event.key in dirkeys:
                        level.player.try_move(dirkeys.index(event.key))
                        
                    if event.key == K_RETURN:
                        return
                            
                            
            # execute frame for all sprites in layer order
            for sprite in level.sprites.sprites():
                sprite.start_turn()
                sprite.do_move(elapsed)
            
            # get offset and draw background
            left, top = self.find_offset(level)
            self.view.blit(self.background, (0, 0), (left, top, self.width, self.height))

            # update sprite positions, check for collisions, draw sprites
            level.sprites.update(self.cellsize, (left, top), self.tileset)
            for sprite in level.sprites.sprites():
                sprite.check_collisions()
                
            # check for death
            if not level.player.alive():
                sys.exit('Ouch!')
            if not level.rover.alive():
                sys.exit('Arf!')
            
            # check for win condition
            if level.player.done_level():
                return
                
            level.sprites.draw(self.view)

            # update display
            pygame.display.update()



if __name__ == '__main__':
    Roverchip('levels.txt', 'tiles.png', 16)
