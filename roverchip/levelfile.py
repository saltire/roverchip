import re

import level


class LevelFile:
    def __init__(self, path):
        with open(path) as lfile:
            self.lines = [line.strip() for line in lfile.readlines() if line.strip() and line[0] != '#']
            
    
    def get_levels(self):
        levels = []
            
        for i, startline in enumerate(self.lines):
            if startline[0] == '!':
                i += 1
                
                try:
                    # collect map data
                    mapdata = []
                    width = None
                    while True:
                        if width is None:
                            width = len(self.lines[i])
                        if not self.lines[i].isdigit() or len(self.lines[i]) != width:
                            break
                        mapdata.append(self.lines[i])
                        i += 1
                            
                    # collect sprite data
                    sprites = {}
                    while True:
                        match = re.match('(\w+):\s*((\d+,\s*)*\d+)', self.lines[i])
                        if not match:
                            break
                        sprites.setdefault(match.group(1), []).append(tuple(int(x) for x in match.group(2).split(',')))
                        i += 1
                
                except IndexError:
                    pass # eof
                
                if not mapdata or not sprites:
                    raise Exception('invalid level format at line {0}:\n{1}'.format(i, self.lines[i]))
                
                for item in ('player', 'rover', 'exit'):
                    if item not in sprites:
                        raise Exception('missing level data: {0}'.format(item))
                
                levels.append(level.Level(mapdata, sprites))

        return levels
