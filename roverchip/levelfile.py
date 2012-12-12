from collections import Counter
import re

import level
from sprites import spritetypes


class LevelFile:
    cells = {'-': ('Floor',),
             '0': ('Wall',),
             'x': ('Fire',),
             'W': ('Water',),
             '^': ('Water', 0), # n
             '>': ('Water', 1), # e
             'v': ('Water', 2), # s
             '<': ('Water', 3), # w
             '=': ('Grate',),
             '*': ('Exit',)
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
                    
                if not all(ctype in self.cells for ctype in line):
                    break
                for x, ctype in enumerate(line):
                    celldata[x, i - starti - 1] = (self.cells[ctype][0], self.cells[ctype][1:])
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
