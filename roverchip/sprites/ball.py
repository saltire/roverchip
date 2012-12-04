import sprite


class Ball(sprite.Sprite):   
    def __init__(self, level, pos):
        sprite.Sprite.__init__(self, level, pos)
        self.colour = (255, 128, 128)
        self.speed = 5
        self.is_movable = 1
        self.is_solid = 1
        
    
    def after_move(self):
        nextcell = self.level.get_neighbour(self.pos, self.facing)

        if (self.level.get_cell(self.pos).get_type() == 'Water'
            and not self.level.get_sprites_in(self.pos, False, 'SunkenCrate')):
            self.kill()
        
        elif self.level.object_can_enter(nextcell) and not self.level.get_solid_sprites_in(nextcell):
            self.to_move = 1
            