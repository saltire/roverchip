from collections import Counter
import re

import level


class LevelFile:
    cells = {'-': ('floor',),
             '0': ('wall',),
             'x': ('fire',),
             'W': ('water',),
             '^': ('water', 0), # n
             '>': ('water', 1), # e
             'v': ('water', 2), # s
             '<': ('water', 3), # w
             '=': ('grate',),
             '*': ('exit',)
             }
    
    sprites = ['ball', 'cart', 'chip', 'chipdoor', 'crate', 'door', 'key', 'laser', 'mirror',
               'player', 'robot', 'rover', 'shooter', 'tank']
    
    
    def __init__(self, path):
        with open(path) as lfile:
            self.lines = [(linenum, line.strip()) for linenum, line in enumerate(lfile)
                          if line.strip() and line[0] != '#']
            
    
    def get_levels(self):
        """Read level data from the text file. This is a quick, dirty,
        temporary level format."""
        levels = []
            
        for i, startline in enumerate(self.lines):
            if startline[1][0] == '!':
                i += 1
                starti = i
                
                celldata = {}
                spritedata = []
                
                try:
                    # collect map data
                    width = None
                    while True:
                        linenum, line = self.lines[i]
                        
                        if width is None:
                            width = len(line)
                            
                        if not all(ctype in self.cells for ctype in line):
                            break
                        celldata.update({(x, i - starti): self.cells[ctype]
                                        for x, ctype in enumerate(line)})
                        i += 1
                        
                    if not celldata:
                        raise Exception('invalid level format at line {0}:\n{1}'
                                        .format(linenum, line))
                            
                    # collect sprite data
                    while True:
                        linenum, line = self.lines[i]
                        
                        match = re.match('(\w+):\s*(((\d+,\s*)*\d+\s*)+)', line)
                        if not match:
                            break
                        
                        if match.group(1).lower() not in self.sprites:
                            raise Exception('invalid sprite data at line {0}:\n{1}'
                                            .format(linenum, line))
                        
                        for sdata in match.group(2).split():
                            spritedata.append((match.group(1),)
                                              + tuple(int(x) for x in sdata.split(',')))
                        i += 1
                
                except IndexError:
                    pass # eof
                
                # check for illegal counts of cells and sprites
                ccount = Counter(cell[0] for cell in celldata.values())
                scount = Counter(sprite[0] for sprite in spritedata)
                if ccount['exit'] != 1:
                    raise Exception('must be exactly 1 exit in level {0}'
                                    .format(len(levels) + 1))
                if scount['player'] != 1:
                    raise Exception('must be exactly 1 player in level {0}'
                                    .format(len(levels) + 1))
                if scount['rover'] == 0 and scount['chip'] == 0:
                    raise Exception('must be at least 1 rover or chip in level {0}'
                                    .format(len(levels) + 1))
                
                levels.append(level.Level(celldata, spritedata))

        return levels
