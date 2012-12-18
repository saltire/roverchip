from collections import Counter
import re

import level
from sprites import spritetypes


class LevelFile:
    cells = {'-': ('Floor',),
             '0': ('Wall',),
             'x': ('Fire',),
             'W': ('Water', {'W': (None,), '^': (0,), '>': (1,), 'v': (2,), '<': (3,)}),
             '=': ('Grate',),
             '*': ('Exit',),
             '/': ('Ice', {'/': (None,), '^': (0,), '>': (1,), 'V': (2,), '<': (3,)}),
             'C': ('Conveyor', {'^': (0,), '>': (1,), 'v': (2,), '<': (3,)}),
             '.': ('Button', {'%': (0,), 'S': (1,), 'T': (2,)}),
             '%': ('Toggle', {'0': (0,), '1': (1,)}),
             '[': ('Door', {'0': (1, 0), '1': (1, 1), '2': (1, 2), '3': (1, 3)}),
             ']': ('Door', {'0': (2, 0), '1': (2, 1), '2': (2, 2), '3': (2, 3)}),
             '{': ('ChipDoor', {'-': (0,), '|': (1,)})
             }
    
    
    def __init__(self, path):
        with open(path) as lfile:
            self.lines = [(linenum, line.strip()) for linenum, line in enumerate(lfile)
                          if line.strip() and line[0] != '#']
            
    
    def get_levels(self):
        """Read level data from the text file. This is a quick, dirty,
        temporary level format."""
        levels = []
            
        for starti, startline in enumerate(self.lines):
            if startline[1][0] != '!':
                continue
            
            i = starti + 1
            
            # collect cell data
            celldata = {}
            width = None
            while True:
                try:
                    linenum, line = self.lines[i]
                except IndexError:
                    break
                
                if width is None:
                    width = len(line)
                    
                if not all(len(cell) == 2 and cell[0] in self.cells for cell in line.split()):
                    break
                for x, (ctype, opt) in enumerate(line.split()):
                    cdata = tuple(self.cells[ctype][1][opt]) if len(self.cells[ctype]) > 1 else ()
                    celldata[x, i - starti - 1] = (self.cells[ctype][0], cdata)
                i += 1
                
            # check cell requirements
            if not celldata:
                raise Exception('invalid level format at line {0}:\n{1}'
                                .format(linenum, line))
            ccount = Counter(cell[0] for cell in celldata.values())
            if ccount['Exit'] != 1:
                raise Exception('must be exactly 1 exit in level {0}'
                                .format(len(levels) + 1))
                    
            # collect sprite data
            spritedata = []
            while True:
                try:
                    linenum, line = self.lines[i]
                except IndexError:
                    break
                
                match = re.match('(\w+):\s*(((\d+,\s*)*\d+\s*)+)', line)
                if not match:
                    break
                
                try:
                    stype = next(stype for stype in spritetypes
                                 if stype.lower() == match.group(1).lower())
                except StopIteration:
                    raise Exception('invalid sprite data at line {0}:\n{1}'
                                    .format(linenum, line))
                
                for sdata in match.group(2).split():
                    sdata = tuple(int(x) for x in sdata.split(','))
                    spritedata.append((stype, sdata[0:2], sdata[2:]))
                i += 1
            
            # check sprite requirements
            scount = Counter(sprite[0] for sprite in spritedata)
            if scount['Player'] != 1:
                raise Exception('must be exactly 1 player in level {0}'
                                .format(len(levels) + 1))
            if scount['Rover'] == 0 and scount['Chip'] == 0:
                raise Exception('must be at least 1 rover or chip in level {0}'
                                .format(len(levels) + 1))
            
            # instantiate level
            levels.append(level.Level(celldata, spritedata))

        return levels
