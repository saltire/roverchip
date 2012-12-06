import sprite


class Cart(sprite.Sprite):   
    def __init__(self, level, pos):
        sprite.Sprite.__init__(self, level, pos)
        self.tile = 1, 1
        self.speed = 5
        self.is_movable = True
        self.is_solid = True
        
    
    def after_move(self):
        nextcell = self.level.get_neighbour(self.pos, self.facing)

        if self.level.object_can_enter(nextcell) and not self.level.get_solid_sprites_in(nextcell):
            self.to_move = 1
