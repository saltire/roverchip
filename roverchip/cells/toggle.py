from cell import Cell


class Toggle(Cell):
    def __init__(self, level, pos, state):
        Cell.__init__(self, level, pos)
        
        self.tile = 11, 0
        self.player_can_enter = not state
        self.robot_can_enter = not state
        self.object_can_enter = not state

        self.state = bool(state)
        self.off_tile = 0, 0
        self.on_tile = 1, 0
        
        
    def draw(self, cellsize, tileset):
        """Draw either a floor or a wall, with the toggle border added."""
        tile = self.on_tile if self.state else self.off_tile
        tileimg = tileset.get_tile(tile).copy()
        borderimg = tileset.get_tile(self.tile)
        tileimg.blit(borderimg, (0, 0))
        return tileimg
    
    
    def toggle_state(self):
        """Toggle the cell between wall and floor, and redraw the tile."""
        self.state = not self.state
        
        self.player_can_enter = not self.state
        self.robot_can_enter = not self.state
        self.object_can_enter = not self.state
        
        self.level.trigger_redraw(self.pos)

        