import sprite


class Crate(sprite.Sprite):   
    def __init__(self, level, pos):
        sprite.Sprite.__init__(self, level, pos)
        self.colour = (128, 128, 128)
        self.is_movable = 1
        self.is_solid = 1
        
        
    def after_move(self):
        if self.level.get_cell(self.pos).get_type() == 'Fire':
            self.to_move = 1
        
        elif (self.level.get_cell(self.pos).get_type() == 'Water'
              and not self.level.get_sprites_in(self.pos, 0, 'SunkenCrate')):
            self.kill()
            
            sunken = SunkenCrate(self.level, self.pos)
            self.level.sprites.add(sunken)
            sunken.after_move()



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