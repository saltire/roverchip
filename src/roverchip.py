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
        self.tilesize = 100
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
        for x in range(self.map.width):
            for y in range(self.map.height):
                rect = x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize
                if self.map.get_blocktype((x, y)) == 1:
                    self.background.fill((0, 0, 0), rect)
                else:
                    self.background.fill((255, 255, 255), rect)
        self.screen.blit(self.background, (0, 0))

        # draw mobs
        self.map.mobs.update(self.tilesize)
        self.map.mobs.draw(self.screen)

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
                    
                    for mob in self.map.mobs:
                        mob.set_size(self.tilesize)
                        
                    self.init_screen(event.size)
                    
                # move controls
                elif event.type == KEYDOWN:
                    if event.key in dirkeys:
                        for player in self.map.player:
                            player.start_move(dirkeys.index(event.key))
                            
            # check if enemies need to move
            for enemy in self.map.enemies:
                enemy.start_move()
            
            # update mobs
            self.map.mobs.update(self.tilesize, elapsed)
            collide = pygame.sprite.groupcollide(self.map.player, self.map.enemies, 0, 0)
            if collide:
                for player in collide:
                    print player
                    for enemy in collide[player]:
                        print enemy
                break
            
            # update laserbeams
            for laser in self.map.lasers:
                laser.calculate_path()
            self.map.beams.update(self.tilesize)
                
            # clear and draw
            self.map.mobs.clear(self.screen, self.background)
            self.map.beams.clear(self.screen, self.background)
            updates = self.map.mobs.draw(self.screen)
            updates += self.map.beams.draw(self.screen)

            # update display
            pygame.display.update(updates)


if __name__ == '__main__':
    game = Roverchip()