import sprite


class Ball(sprite.Sprite):   
    def __init__(self, level, pos):
        sprite.Sprite.__init__(self, level, pos)
        
        self.tile = 0, 1
        self.speed = 5
        self.is_movable = True
        self.is_solid = True
        
        
    def start_turn(self):
        # if it's entirely on a water cell, destroy it
        if (len(self.cells_in()) == 1
            and self.level.get_cell(self.pos).get_type() == 'Water'
            and not self.level.get_sprites_in(self.pos, False, 'SunkenCrate')
            ):
            self.kill()
        
    
    def after_move(self):
        nextcell = self.level.get_neighbour(self.pos, self.move_dir)
        if self.level.object_can_enter(nextcell) and not self.level.get_solid_sprites_in(nextcell):
            self.to_move = 1
            