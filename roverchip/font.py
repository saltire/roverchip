import pygame


class Font:
    def __init__(self, spritepath, charsize, mono=False, spacewidth=None):
        """Given a sprite that is a grid of characters, and the dimensions
        of each character, slice it into a dict of surfaces mapped to each
        character in ASCII sequence, starting at 0."""
        self.sprite = pygame.image.load(spritepath)
        cw, ch = charsize
        sw, sh = self.sprite.get_width() / cw, self.sprite.get_height() / ch
        spacewidth = spacewidth if spacewidth is not None else cw * .4
        
        self.height = ch

        self.chars = {}
        for y in range(sh):
            for x in range(sw):
                char = chr(x + y * sw)
                charimg = self.sprite.subsurface((x * cw, y * ch, cw, ch))
                
                # crop characters to their actual width, unless monospaced
                if not mono:
                    cwidth = (charimg.get_bounding_rect()[2]
                              if char != ' ' else spacewidth)
                    charimg = charimg.subsurface((0, 0, cwidth, ch))
                    
                self.chars[char] = charimg
    
    
    def render(self, text, lineheight=None, leading=0, kerning=1, color=None):
        """Return a surface containing a graphical rendering of the text.
        If lineheight is passed, scale the characters to that height.
        Color will replace all colours, keeping alpha unchanged.
        Takes a string or a list of strings (formatting the characters once)."""
        # return the glyphs for each unique character in a block of text
        def format_chars(text):
            chars = {char: self.chars[char] for char in set(text.replace('\n', ''))}
            scale = 1.0 if lineheight is None else float(lineheight) / self.height
            
            for char, charimg in chars.iteritems():
                if color is not None:
                    # replace RGB channels with those from color
                    pix = pygame.surfarray.pixels3d(charimg)
                    pix[:,:,0], pix[:,:,1], pix[:,:,2] = color
                    del(pix)
                    
                if leading > 0 or kerning > 0:
                    # replace the character surface with a larger one
                    chars[char] = pygame.Surface((charimg.get_width() + kerning,
                                                  charimg.get_height() + leading),
                                                 pygame.SRCALPHA)
                    chars[char].blit(charimg, (0, 0))
                
                if scale != 1.0:
                    # scale character to the line height
                    charwidth = int(chars[char].get_width() * scale)
                    chars[char] = pygame.transform.scale(chars[char],
                                                         (charwidth, int(lineheight)))
                    
            return chars
        
        # render the block of text using the given glyphs
        def render_text(text, chars):
            text = text.split('\n')
            width = max(sum(chars[char].get_width() for char in line)
                        for line in text)
            height = (lineheight + leading) * len(text) - leading
            canvas = pygame.Surface((width, height), pygame.SRCALPHA)
            
            for y, line in enumerate(text):
                x = 0
                for char in line:
                    canvas.blit(chars[char], (x, y * (lineheight + leading)))
                    x += chars[char].get_width()
                    
            return canvas
        
        if isinstance(text, str):
            # render a string
            return render_text(text, format_chars(text))
        
        else:
            # format all characters at once and render multiple strings
            chars = format_chars(''.join(text))
            return [render_text(t, chars) for t in text]
        

