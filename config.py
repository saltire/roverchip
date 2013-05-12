import os


path = lambda p: os.path.join(os.path.dirname(__file__), 'roverchip', p)


# window

levelpath       = path('levels/*.tmx')
windowsize      = 800, 400
minsize         = 200, 120
keyrepeat       = 100

# menu

menubackcolor   = 255, 255, 255
menufontcolor   = 0, 0, 0
menuratio       = 3, 2
menumargin      = 0.05, 0.05
textmargin      = 0.05, 0.1
        
menufontpath    = path('font.png')
menufontsize    = 8, 8

maxrows         = 8
maxfontsize     = 96
minfontsize     = 8
sizestep        = 8
columns         = 2
leadpct         = 0.4

# game

tilepath        = path('tiles.png')
tilesize        = 16, 16
