import sys

import pygame
from pygame.locals import *

import map

class Roverchip:
    
    def __init__(self):
        pygame.init()
        
        # init clock
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick()

        # init keyboard settings
        pygame.key.set_repeat(1, 50)

        # init map
        self.map = map.Map()
        self.tilesize = 75
        dims = self.map.width * self.tilesize, self.map.height * self.tilesize
        
        # init screen
        self.init_screen(dims)
        
        # start loop
        self.loop()
        
        
    def init_screen(self, dims):
        # init window and background
        self.screen = pygame.display.set_mode(dims, RESIZABLE)
        self.background = pygame.Surface(dims)
        
        # draw background
        for x, y in self.map.colours:
            rect = x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize
            self.background.fill(self.map.colours[(x, y)], rect)
        self.screen.blit(self.background, (0, 0))

        # draw sprites
        self.map.sprites.update(self.tilesize)
        self.map.sprites.draw(self.screen)

        # update display
        pygame.display.update()

        
    def loop(self):
        dirkeys = [K_UP, K_RIGHT, K_DOWN, K_LEFT]
        
        while 1:
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
                    width, height = event.size
                    self.tilesize = min(width / self.map.width, height / self.map.height)
                    self.init_screen(event.size)
                    
                # move controls
                elif event.type == KEYDOWN:
                    if event.key in dirkeys:
                        for player in self.map.get_objects('Player'):
                            player.try_move(dirkeys.index(event.key))
                            
                            
            # clear and update sprites
            self.map.sprites.clear(self.screen, self.background)
            
            # execute frame for all sprites in layer order
            for sprite in self.map.sprites.sprites():
                sprite.do_turn(elapsed)
            
            # update positions, check for collisions
            self.map.sprites.update(self.tilesize)
            for sprite in self.map.sprites.sprites():
                sprite.check_collisions()
                
            # draw sprites
            updates = self.map.sprites.draw(self.screen)

            # update display
            pygame.display.update(updates)


if __name__ == '__main__':
    game = Roverchip()