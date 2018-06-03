from PIL import Image
import os
import math

tilepath = '/Tiles/'

map = [(3, 4), (4, 5), (4, 7), (3, 8), (2, 7), (2, 5),
       (3, 2), (4, 3), (5, 4), (5, 6), (5, 8), (4, 9), (3, 10), (2, 9), (1, 8), (1, 6), (1, 4), (2, 3),
       (4, 1), (5, 2), (6, 5), (6, 7), (5, 10), (4, 11), (2, 11), (1, 10), (0, 7), (0, 5), (1, 2), (2, 1)]

h, w = 490, 530

def init(rootpath):
    global tilepath
    tilepath = rootpath + tilepath

def addMecatol(galaxy, size):
    tilewidth = w
    tileheight = h
    if size == 0:
        tilewidth = int(w * 1/4)
        tileheight = int(h * 1/4)
    if size == 1:
        tilewidth = int(w * 1/2)
        tileheight = int(h * 1/2)
        
    x_adj = tilewidth * 3 / 4
    y_adj = tileheight / 2
    
    system = '18.png'
    tile = Image.open(tilepath + system)
    tile = tile.resize((tilewidth, tileheight), Image.ANTIALIAS)
    x = int(x_adj * 3)
    y = int(y_adj * 6)
    galaxy.paste(tile, (x, y), tile)


def genGalaxy(systems, size):
    tilewidth = w
    tileheight = h
    if size == 0:
        tilewidth = int(w * 1/4)
        tileheight = int(h * 1/4)
    if size == 1:
        tilewidth = int(w * 1/2)
        tileheight = int(h * 1/2)
      
    x_adj = tilewidth * 3 / 4
    y_adj = tileheight / 2
      
    result = Image.new("RGBA", (tilewidth * 7, tileheight * 7))

    systems = systems[:30]

    for index, system in enumerate(systems):
        if int(system) > 50:
            continue
        system = system + '.png'
        tile = Image.open(tilepath + system)
        tile = tile.resize((tilewidth, tileheight), Image.ANTIALIAS)
        x = int(x_adj * map[index][0])
        y = int(y_adj * map[index][1])
        result.paste(tile, (x, y), tile)

    addMecatol(result, size)

    bbox = result.getbbox()
    result = result.crop(bbox)
    #result.save('/tmp/image.png')
    return result
