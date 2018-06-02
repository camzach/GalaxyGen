from random import choice, sample

tiles = list(range(19,51))
slicemap = [[0, 6, 18, 29, 17, 7],
            [1, 8, 19, 20, 7, 9],
            [2, 10, 21, 22, 9, 11],
            [3, 12, 23, 24, 11, 13],
            [4, 14, 25, 26, 13, 15],
            [5, 16, 27, 28, 15, 17]]

#Create definitions for tiles based on tiledef.txt
with open('tiledef.txt') as tiledef_raw:
    tiledef = []
    #Insert 18 empty systems so tiledef[19] reflects system 19
    for x in range(19):
        tiledef.append(None)
    #Read data
    raw = [line.replace('\n', '').split('\t') for line in tiledef_raw]
    for tile in raw:
        tiledef.append({'res': int(tile[0]),
                        'inf': int(tile[1]),
                        'tech': int(tile[2]),
                        'haz': int(tile[3]),
                        'cul': int(tile[4]),
                        'ind': int(tile[5]),
                        'anom': int(tile[6])})
#Create adjacency matrix
with open('adjacencymatrix.txt') as adjmatrix_raw:
    adjmap = []
    for line in adjmatrix_raw:
        adjmap.append(list(map(int, line.replace('\n', '').split('\t'))))

def scoreGalaxy(slices):
    scores = []
    for slice in slices:
        #Resource score = (4*sum of home res + 1/2*sum of equidistant res)*2
        res = sum(tiledef[slice[x]]['res'] for x in range(4)) * 4
        res += sum(tiledef[slice[x]]['res'] for x in range(4, 6)) * 1/2
        res *= 2
        #Influence score = 2*sum of home ing + sum of equidistant inf
        inf = sum(tiledef[slice[x]]['inf'] for x in range(4)) * 2
        inf += sum(tiledef[slice[x]]['inf'] for x in range(4, 6))
        #Tech score depends on number of tech planets, equidistant count as 1/2
        tech = sum(tiledef[slice[x]]['tech'] for x in range(4))
        tech += sum(tiledef[slice[x]]['tech'] for x in range(4, 6)) * 1/2
        tech = -1 if tech == 0 else tech * 2 - 1
        #Trait score = (missing: -2, single: -1, double: 0, 3+: 3)
        haz = sum(tiledef[slice[x]]['haz'] for x in range(6))
        haz = haz - 2 if haz < 3 else 3
        cul = sum(tiledef[slice[x]]['cul'] for x in range(6))
        cul = cul - 2 if cul < 3 else 3
        ind = sum(tiledef[slice[x]]['ind'] for x in range(6))
        ind = ind - 2 if ind < 3 else 3
        trait = haz + cul + ind
        #Sum the scores
        score = res + inf + tech + trait
        #Append to scores list
        scores.append({'res': res, 'inf': inf, 'tech': tech, 'trait': trait, 'score': score})
    return scores

def generateGalaxy():
    systems = []
    while not all(x in systems for x in [25, 26, 39, 40]):
        systems = sample(tiles, 30)
    slices = [list(map(lambda x: systems[x], slice)) for slice in slicemap]
    scores = scoreGalaxy(slices)
    return (systems, slices, scores)

def checkMapValidity(systems):
    for location, system in enumerate(systems):
        adjacency = list(map(lambda x: systems[x], adjmap[location]))
        if system in [25, 26]:
            print(system)
            if (system + 15 + 2 * (25 - system)) in adjacency:
                return False
        if system in [41, 42, 43, 44, 45]:
            print(system)
            if any(x in adjacency for x in [41, 42, 43, 44, 45]):
                return False
    return True

def generateBalancedMap():
    bestSystems = None
    bestSlices = None
    bestScores = None
    bestRange = 99999
    x = 0
    while x < 1:
        systems, slices, scores = generateGalaxy()
        if not checkMapValidity(systems):
            continue
        sliceRange = (max(score['score'] for score in scores)
                    - min(score['score'] for score in scores))
        if sliceRange < bestRange:
            bestSystems = systems
            bestSlices = slices
            bestScores = scores
            bestRange = sliceRange
        x += 1
    print(bestSystems)
    print(bestSlices)
    print(bestScores)
    print(bestRange)
