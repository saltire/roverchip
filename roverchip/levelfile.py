from collections import Counter
import re

import level


class LevelFile:
    cells = [('floor',),
             ('wall',),
             ('fire',),
             ('water',),
             ('water', 0), # n
             ('water', 1), # e
             ('water', 2), # s
             ('water', 3), # w
             ('grate',),
             ('exit',),
             ]
    
    sprites = ['ball', 'cart', 'crate', 'door', 'key', 'laser', 'mirror',
               'player', 'robot', 'rover', 'shooter', 'tank']
    
    
    def __init__(self, path):
        with open(path) as lfile:
            self.lines = [line.strip() for line in lfile if line.strip() and line[0] != '#']
            
    
    def get_levels(self):
        """Read level data from the text file. This is a quick, dirty,
        temporary level format."""
        levels = []
            
        for i, startline in enumerate(self.lines):
            if startline[0] == '!':
                i += 1
                starti = i
                
                celldata = {}
                spritedata = []
                
                try:
                    # collect map data
                    width = None
                    while True:
                        if width is None:
                            width = len(self.lines[i])
                        if not self.lines[i].isdigit() or len(self.lines[i]) != width:
                            break
                        celldata.update({(x, i - starti): self.cells[int(celltype)]
                                        for x, celltype in enumerate(self.lines[i])})
                        i += 1
                        
                    if not celldata:
                        raise Exception('invalid level format at line {0}:\n{1}'.format(i, self.lines[i]))
                            
                    # collect sprite data
                    while True:
                        match = re.match('(\w+):\s*((\d+,\s*)*\d+)', self.lines[i])
                        if not match:
                            break
                        
                        if match.group(1) not in self.sprites:
                            raise Exception('invalid sprite data at line {0}'.format(i))
                        
                        spritedata.append((match.group(1),)
                                       + tuple(int(x) for x in match.group(2).split(',')))
                        i += 1
                
                except IndexError:
                    pass # eof
                
                # check that there is exactly 1 exit
                if Counter(celldata.values())[('exit',)] != 1:
                    raise Exception('should be exactly 1 exit in level {0}'.format(len(levels) + 1))
                
                # check that there is exactly 1 player and 1 rover
                for stype in ('player', 'rover'):
                    scount = len([True for sprite in spritedata if sprite[0] == stype])
                    if scount == 0:
                        raise Exception('missing {0} data in level {1}'.format(stype, len(levels) + 1))
                    elif scount > 1:
                        raise Exception('multiple {0} data in level {1}'.format(stype, len(levels) + 1))
                    
                
                levels.append(level.Level(celldata, spritedata))

        return levels
