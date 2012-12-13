import cell


class Button(cell.Cell):
    def __init__(self, level, pos, colour):
        cell.Cell.__init__(self, level, pos)
        
        self.tile = 9, 2 + colour
        
        self.colour = colour


    def trigger_button(self):
        """Trigger actions that occur when a sprite touches the button."""
        # green button: toggle walls
        if self.colour == 0:
            for cell in self.level.get_cells('Toggle'):
                cell.toggle_state()

        # blue button: rotate sentries
        elif self.colour == 1:
            for sentry in self.level.get_sprites('Sentry'):
                sentry.facing = (sentry.facing + 2) % 4
                sentry.move_dir = sentry.facing
                sentry.to_move = 1


    def player_inside(self):
        self.trigger_button()
        
        
    def enemy_inside(self):
        self.trigger_button()
        
        
    def object_inside(self):
        self.trigger_button()
