import sys

import pygame

from screens import game
from screens import menu
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
        
        # init screen
        screen = menu.Menu()
        #screen = game.Game(tiledmap.TiledMap(levelpath).get_levels())
            
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
                if event.type == pygame.QUIT:
                    sys.exit()
                    
                # resize window
                elif event.type == pygame.VIDEORESIZE:
                    self.init_window(event.size)
                    
                elif event.type == pygame.KEYDOWN:
                    keys.append((event.key, 1))
                    
                elif event.type == pygame.KEYUP:
                    keys.append((event.key, 0))
            
            # run a frame of the game
            status = screen.run_frame(elapsed, keys)
            pygame.display.update()
            
            if status[0] == 'win':
                break
            
            if status[0] == 'dead':
                sys.exit(('Ouch!', 'Arf!')[status[1]])
            
        sys.exit('Yay!')
        
        
    def init_window(self, (width, height)):
        """Initialize the game window. Called at beginning, and every time
        the window is resized."""
        pygame.display.set_mode((width, height), pygame.RESIZABLE).fill((0, 0, 0))
        


if __name__ == '__main__':
    Roverchip()
