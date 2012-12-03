import sprite

class SunkenCrate(sprite.Sprite):
    
    def __init__(self, level, pos):
        sprite.Sprite.__init__(self, level, pos)
        self.colour = (128, 128, 128, 128)
        self.speed = 2
        
        
    def after_move(self):
        flow_dir = self.level.get_cell(self.pos).get_flow_dir()
        if (flow_dir is not None
            and not self.level.get_sprites_in(self.level.get_neighbour(self.pos, flow_dir), False, 'SunkenCrate')):
            self.facing = flow_dir
            self.to_move = 1