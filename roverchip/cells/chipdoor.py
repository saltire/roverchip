from cell import Cell


class ChipDoor(Cell):
    def __init__(self, level, pos, facing):
        Cell.__init__(self, level, pos)
        
        self.tile = 7, 3 + (facing % 2)
        self.player_can_enter = False
        self.robot_can_enter = False
        self.object_can_enter = False
        
        self.floor_tile = 0, 0


    def draw(self, cellsize, tileset):
        """Draw the ice tile, then draw the rotated corner on top of it."""
        tileimg = tileset.get_tile(self.floor_tile).copy()
        doorimg = tileset.get_tile(self.tile)
        tileimg.blit(doorimg, (0, 0))
        
        return tileimg
