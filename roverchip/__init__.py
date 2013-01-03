import sys

import pygame
from pygame.locals import *

import game
import tiledmap


class Roverchip:
    def __init__(self, levelpath='levels/*.tmx'):
        pygame.init()
        
        # init clock
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick()

        # init keyboard settings
        pygame.key.set_repeat(1, 50)

        # init window
        self.dims = (800, 480)
        self.init_window(self.dims)
        
        # run levels
        screen = game.Game(tiledmap.TiledMap(levelpath).get_levels())
            
        # run frame loop
        while True:
            # update clock
            old_time = self.time
            self.time += self.clock.tick(60)
            elapsed = float(self.time - old_time)
            
            # get keypresses
            keys = []
            for event in pygame.event.get():
                # close window
                if event.type == QUIT:
                    sys.exit()
                    
                # resize window
                elif event.type == VIDEORESIZE:
                    self.init_window(event.size)
                    
                elif event.type == KEYDOWN:
                    keys.append((event.key, 1))
                    
                elif event.type == KEYUP:
                    keys.append((event.key, 0))
            
            # run a frame of the game
            status = screen.run_frame(elapsed, keys)
            
            if status[0] == 'win':
                break
            
            if status[0] == 'dead':
                sys.exit(('Ouch!', 'Arf!')[status[1]])
            
        sys.exit('Yay!')
        
        
    def init_window(self, (width, height)):
        """Initialize the game window. Called at beginning, and every time
        the window is resized."""
        pygame.display.set_mode((width, height), RESIZABLE).fill((0, 0, 0))
        


if __name__ == '__main__':
    Roverchip()
