import glob
import xml.etree.ElementTree as xml


class TiledMap:
    tiles = {(0, 0): ('Floor',),
             (1, 0): ('Wall',),
             (2, 0): ('Water',),
             (3, 0): ('Conveyor', ''),
             (4, 0): ('Ice',),
             (5, 0): ('Toggle', 0),
             (6, 0): ('Button', 0),
             (7, 0): ('Door', '', 0),
             (8, 0): ('Door', '', 1),
             (9, 0): ('Door', '', 2),
             (10, 0): ('Door', '', 3),
             (11, 0): ('ChipDoor', ''),
             (0, 1): ('Grate',),
             (1, 1): ('Fire',),
             (2, 1): ('Water', ''),
             (4, 1): ('Ice', ''),
             (5, 1): ('Toggle', 1),
             (6, 1): ('Button', 1),
             (0, 2): ('Exit',),
             (1, 2): ('Mud',),
             (0, 4): ('Ball',),
             (1, 4): ('Cart',),
             (2, 4): ('Crate',),
             (3, 4): ('Laser', ''),
             (4, 4): ('Mirror', ''),
             (5, 4): ('Dirt',),
             (7, 4): ('Key', 0),
             (8, 4): ('Key', 1),
             (9, 4): ('Key', 2),
             (10, 4): ('Key', 3),
             (11, 4): ('Chip',),
             (0, 5): ('Player', ''),
             (1, 5): ('Rover', ''),
             (2, 5): ('Shooter', ''),
             (3, 5): ('Robot', '', 0),
             (4, 5): ('Tank', '', 1),
             (5, 5): ('Sentry', ''),
             (7, 5): ('Boots', 0),
             (8, 5): ('Boots', 1),
             (9, 5): ('Boots', 2),
             (10, 5): ('Boots', 3),
             (3, 6): ('Robot', '', 1),
             (4, 6): ('Tank', '', 2),
             }

    def __init__(self, pattern):
        """Parse all Tiled XML files matching the given pattern."""
        self.levels_xml = ((lfile.strip('.tmx'), xml.parse(lfile)) for lfile in glob.glob(pattern))
        
        
    def get_levels(self):
        """For each file passed, get cell data from the first layer
        and sprite data from the rest, and instantiate a level."""
        
        def get_tile_data(layer, width, height):
            layerdata = layer.find('data').text.split(',')
            tiledata = {}
            for y in range(height):
                for x in range(width):
                    tile = int(layerdata[y * width + x])
                    if tile:
                        tilenum = tile % 0x10000000 - 1
                        tiletype = self.tiles[tilenum % 16, tilenum / 16]
                        rotate = (0, 10, 12, 6).index(tile / 0x10000000)
                        tiledata[x, y] = (tiletype[0], tuple(rotate if i == '' else i
                                                             for i in tiletype[1:]))
            return tiledata
        
        levels = []
        for filename, lxml in self.levels_xml:
            width = int(lxml.getroot().get('width'))
            height = int(lxml.getroot().get('height'))
            layers = lxml.findall('layer')
            
            # interpret bottom layer as tiles            
            celldata = get_tile_data(layers[0], width, height)
            
            # interpret all subsequent layers as sprites
            spritedata = []
            for layer in layers[1:]:
                spritetiles = get_tile_data(layer, width, height)    
                spritedata.extend((pos, stype, sdata) for pos, (stype, sdata) in spritetiles.items())
            
            levels.append((celldata, spritedata))

        return levels
        
        
