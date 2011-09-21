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
        self.map = map.Map(1)

        # init window
        tilesize = 75
        self.viewsize = (10, 6)
        vw, vh = self.viewsize
        self.init_window((vw * tilesize, vh * tilesize))
        
        # start loop
        self.loop()
        
        
    def init_window(self, (width, height)):
        # init window and background
        self.window = pygame.display.set_mode((width, height), RESIZABLE)
        self.window.fill((0, 0, 0))
        
        # init screen of proper size within the window
        vw, vh = self.viewsize
        self.tilesize = min(width / vw, height / vh)
        self.width, self.height = vw * self.tilesize, vh * self.tilesize
        self.left, self.top = int((width - self.width) / 2), int((height - self.height) / 2)
        self.view = self.window.subsurface((self.left, self.top, self.width, self.height))

        # init background
        self.background = pygame.Surface((self.map.width * self.tilesize, self.map.height * self.tilesize))
        for x, y in self.map.colours:
            rect = x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize
            self.background.fill(self.map.colours[(x, y)], rect)
            
        # draw background
        left, top = self.find_offset()
        self.view.blit(self.background, (0, 0), (left, top, self.width, self.height))

        # draw sprites
        self.map.sprites.update(self.tilesize, (left, top))
        self.map.sprites.draw(self.view)

        # update display
        pygame.display.update()
        
        
    def find_offset(self):
        px, py = self.map.get_objects('Player')[0].pos
        vw, vh = self.viewsize
        
        # find offset that places the player in the centre
        ox = px - (vw - 1) / 2.0
        oy = py - (vh - 1) / 2.0
        
        # clamp values so as not to go off the edge
        left = max(0, min(ox, self.map.width - vw))
        top = max(0, min(oy, self.map.height - vh))
        
        return int(left * self.tilesize), int(top * self.tilesize)

        
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
                     self.init_window(event.size)
                    
                # move controls
                elif event.type == KEYDOWN:
                    if event.key in dirkeys:
                        for player in self.map.get_objects('Player'):
                            player.try_move(dirkeys.index(event.key))
                            
                            
            # execute frame for all sprites in layer order
            for sprite in self.map.sprites.sprites():
                sprite.do_turn(elapsed)
            
            # get offset and draw background
            left, top = self.find_offset()
            self.view.blit(self.background, (0, 0), (left, top, self.width, self.height))

            # update sprite positions, check for collisions, draw sprites
            self.map.sprites.update(self.tilesize, (left, top))
            for sprite in self.map.sprites.sprites():
                sprite.check_collisions()
            self.map.sprites.draw(self.view)

            # update display
            pygame.display.update()


if __name__ == '__main__':
    Roverchip()
