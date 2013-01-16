import pygame


class Font:
    def __init__(self, spritepath='font.png', charsize=(8, 8)):
        """Given a sprite that is a grid of characters, and the dimensions
        of each character, slice it into a dict of surfaces mapped to each
        character in ASCII sequence, starting at 0."""
        self.sprite = pygame.image.load(spritepath)
        cw, ch = charsize
        sw, sh = self.sprite.get_width() / cw, self.sprite.get_height() / ch
        
        self.height = ch
        
        self.chars = {}
        for y in range(sh):
            for x in range(sw):
                char = self.sprite.subsurface((x * cw, y * ch, cw, ch))
                cwidth = char.get_bounding_rect()[2]
                self.chars[chr(x + y * sw)] = char.subsurface((0, 0, cwidth, ch))
    
    
    def render_text(self, text, scale=1, kerning=1, leading=1):
        """Return a surface containing a graphical rendering of the text."""
        text = text.split('\n')
        width = max(sum(self.chars[char].get_width() + kerning for char in line)
                    - kerning
                    for line in text)
        height = self.get_height(len(text), leading)
        canvas = pygame.Surface((width, height))
        
        for y, line in enumerate(text):
            x = 0
            for char in line:
                canvas.blit(self.chars[char], (x, y * (self.height + leading)))
                x += self.chars[char].get_width() + kerning
                
        return (canvas if scale == 1 else
                pygame.transform.scale(canvas, (width * scale, height * scale)))

    
    def get_height(self, lines=1, leading=0):
        """Return the height of the given number of lines at the given leading."""
        return (self.height + leading) * lines