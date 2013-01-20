from ConfigParser import ConfigParser


class Config(ConfigParser):
    def __init__(self, path, section):
        ConfigParser.__init__(self)
        self.read(path)
        self.section = section
        

    def _get(self, section, conv, option):
        return conv(self.get(option))


    def get(self, option):
        return ConfigParser.get(self, self.section, option)

        
    def getint(self, option):
        return ConfigParser.getint(self, self.section, option)

        
    def getfloat(self, option):
        return ConfigParser.getfloat(self, self.section, option)

        
    def getboolean(self, option):
        return ConfigParser.getboolean(self, self.section, option)

        
    def getlist(self, option):
        return [item.strip() for item in self.get(option).split(',')]
    
    
    def getints(self, option):
        return [int(item.strip()) for item in self.get(option).split(',')]


    def getfloats(self, option):
        return [float(item.strip()) for item in self.get(option).split(',')]

