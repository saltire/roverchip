import sys

import pygame
from pygame.locals import *

import tiledmap


class Roverchip:
    move_keys = K_UP, K_RIGHT, K_DOWN, K_LEFT
        
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
        for level in tiledmap.TiledMap(levelpath).get_levels():
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
        

    def loop(self, level):
        """The event loop for the running level."""
        # generate level background
        background = pygame.Surface((level.width * self.cellsize, level.height * self.cellsize))
        for cx, cy in level.cells:
            background.blit(level.get_cell((cx, cy)).draw(self.cellsize, self.tileset),
                            (cx * self.cellsize, cy * self.cellsize))
         
        while True:
            # check for tiles that need to be redrawn
            for cx, cy in level.redraw_cells:
                background.blit(level.get_cell((cx, cy)).draw(self.cellsize, self.tileset),
                                (cx * self.cellsize, cy * self.cellsize))
            level.redraw_cells.clear()
                    
            # find offset that places the player in the centre
            px, py = level.player.pos
            vw, vh = self.viewsize
            ox = px - (vw - 1) / 2.0
            oy = py - (vh - 1) / 2.0
            
            # clamp values so as not to go off the edge
            ox = max(0, min(ox, level.width - vw))
            oy = max(0, min(oy, level.height - vh))

            # blit background onto the view
            left, top = int(ox * self.cellsize), int(oy * self.cellsize)
            self.view.blit(background, (0, 0), (left, top, self.width, self.height))

            # update sprite positions, draw sprites, update display
            level.sprites.update(self.cellsize, (left, top), self.tileset)
            level.sprites.draw(self.view)
            pygame.display.update()

            # check collisions
            for sprite in level.sprites.sprites():
                sprite.check_collisions()

            # check for death
            if not level.player.alive():
                sys.exit('Ouch!')
            if any(not rover.alive() for rover in level.get_sprites('Rover')):
                sys.exit('Arf!')
            
            # check for win condition
            if level.player.done_level():
                return

            # update clock
            old_time = self.time
            self.time += self.clock.tick(60)
            elapsed = float(self.time - old_time)
            
            # handle events
            for event in pygame.event.get():

                # close window
                if event.type == QUIT:
                    sys.exit()
                
                # resize window
                elif event.type == VIDEORESIZE:
                    self.init_window(event.size)
                    level.redraw = True
                    
                # move controls
                elif (event.type == KEYDOWN and event.key in self.move_keys):
                    level.player.move_key_down(self.move_keys.index(event.key))
                        
                elif (event.type == KEYUP and event.key in self.move_keys):
                    level.player.move_key_up(self.move_keys.index(event.key))
                
                # skip level
                elif event.type == KEYDOWN and event.key == K_RETURN:
                        return
                    
            # run hooks for all sprites in layer order
            for sprite in level.sprites.sprites():
                sprite.start_turn()
            for sprite in level.sprites.sprites():
                sprite.do_move(elapsed)
            for sprite in level.sprites.sprites():
                if sprite.new_cell:
                    sprite.after_move()
                    sprite.new_cell = False
            for sprite in level.sprites.sprites():
                sprite.end_turn()



if __name__ == '__main__':
    Roverchip('levels', 'tiles.png', 16)
