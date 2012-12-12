class Cell:
    def __init__(self, level):
        self.level = level
        
        self.tile = 0, 0                # tile coords in the tileset
        self.rotate = 0                 # rotation of the tile
        self.player_can_enter = True    # player can enter this cell
        self.robot_can_enter = True     # robots can enter this cell
        self.object_can_enter = True    # movable objects can enter this cell
        
    
    def get_type(self):
        """Return the type of the cell, i.e. the class name."""
        return self.__class__.__name__
    

    def player_inside(self, pos):
        """A hook that runs after the player fully enters the cell."""
        pass
    