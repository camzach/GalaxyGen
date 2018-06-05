from random import sample, choice

path = '/defs/'

tiles = list(range(19,51))
slicemap = [[0, 6, 18, 29, 17, 7],
            [1, 8, 19, 20, 7, 9],
            [2, 10, 21, 22, 9, 11],
            [3, 12, 23, 24, 11, 13],
            [4, 14, 25, 26, 13, 15],
            [5, 16, 27, 28, 15, 17]]

adjmap = []
tiledef = []
            
def init(rootpath):
    global path
    path = rootpath + '/defs/'
    #Create definitions for tiles based on tiledef.txt
    with open(path + 'tiledef.txt') as tiledef_raw:
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
    with open(path + 'adjacencymatrix.txt') as adjmatrix_raw:
        for line in adjmatrix_raw:
            adjmap.append(list(map(int, line.replace('\n', '').split('\t'))))
        
def scoreGalaxy(systems):
    scores = []
    for slice in range(6):
        #Resource score = (4*sum of home res + 1/2*sum of equidistant res)*2
        res = sum(tiledef[systems[slicemap[slice][x]]]['res'] for x in range(4)) * 4
        res += sum(tiledef[systems[slicemap[slice][x]]]['res'] for x in range(4, 6)) * 1/2
        res *= 2
        #Influence score = 2*sum of home ing + sum of equidistant inf
        inf = sum(tiledef[systems[slicemap[slice][x]]]['inf'] for x in range(4)) * 4
        inf += sum(tiledef[systems[slicemap[slice][x]]]['inf'] for x in range(4, 6)) * 1/2
        #Tech score depends on number of tech planets, equidistant count as 1/2
        tech = sum(tiledef[systems[slicemap[slice][x]]]['tech'] for x in range(4))
        tech += sum(tiledef[systems[slicemap[slice][x]]]['tech'] for x in range(4, 6)) * 1/2
        tech = -1 if tech == 0 else tech * 2 - 1
        #Trait score = (missing: -2, single: -1, double: 0, 3+: 3)
        haz = sum(tiledef[systems[slicemap[slice][x]]]['haz'] for x in range(6))
        haz = haz - 2 if haz < 3 else 3
        cul = sum(tiledef[systems[slicemap[slice][x]]]['cul'] for x in range(6))
        cul = cul - 2 if cul < 3 else 3
        ind = sum(tiledef[systems[slicemap[slice][x]]]['ind'] for x in range(6))
        ind = ind - 2 if ind < 3 else 3
        trait = haz + cul + ind
        #Anomaly penalty
        anom = sum(tiledef[systems[slicemap[slice][x]]]['anom'] for x in range(6))
        #Sum the scores
        score = res + inf + tech + trait + anom
        #Append to scores list
        scores.append({'res': res, 'inf': inf, 'tech': tech, 'trait': trait, 'anom': anom, 'score': score})
    return scores


def balanceGalaxy(systems, scores):
    newSystems = systems[:]
    freeTiles = []
    avg = sum(score['score'] for score in scores)/len(scores)
    for slice in range(6):
        tileContributions = []
        #Score four main systems
        for x in range(4):
            tileContributions.append(tiledef[newSystems[slicemap[slice][x]]]['res'] * 30 +
                                     tiledef[newSystems[slicemap[slice][x]]]['inf'] +
                                     tiledef[newSystems[slicemap[slice][x]]]['tech'] +
                                     tiledef[newSystems[slicemap[slice][x]]]['haz'] +
                                     tiledef[newSystems[slicemap[slice][x]]]['cul'] +
                                     tiledef[newSystems[slicemap[slice][x]]]['ind'] +
                                     tiledef[newSystems[slicemap[slice][x]]]['anom'] * 300)
        #Score equidistant systems
        tileContributions.append(tiledef[newSystems[slicemap[slice][4]]]['res'] +
                                 tiledef[newSystems[slicemap[slice][4]]]['inf'] / 2+
                                 tiledef[newSystems[slicemap[slice][4]]]['tech'] +
                                 tiledef[newSystems[slicemap[slice][4]]]['haz'] +
                                 tiledef[newSystems[slicemap[slice][4]]]['cul'] +
                                 tiledef[newSystems[slicemap[slice][4]]]['ind'] +
                                 tiledef[newSystems[slicemap[slice][4]]]['anom'])
        #Ensure no tile has 0 probability of being chosen
        for y in range(len(tileContributions)):
            if tileContributions[y] < 1:
                tileContributions[y] = 1
        #Remove random tile
        if scores[slice]['score'] > avg:
            probDist = [i for sub in
                        ((x,) * int(tileContributions[x]) for x in range(5))
                        for i in sub]
        else:
            probDist = [i for sub in
                        ((x,) * int(tileContributions[4 - x]) for x in range(5))
                        for i in sub]
        toRemove = choice(probDist)
        freeTiles.append(newSystems[slicemap[slice][toRemove]])
        newSystems[slicemap[slice][toRemove]] = 0
    #Add tiles back in
    while 0 in newSystems:
        toReplace = newSystems.index(0)
        newTile = choice(freeTiles)
        freeTiles.remove(newTile)
        newSystems[toReplace] = newTile
    #Check for improvement
    newScores = scoreGalaxy(newSystems)
    oldRange = (max(scores[slice]['score'] for slice in range(6)) -
                min(scores[slice]['score'] for slice in range(6)))
    newRange = (max(newScores[slice]['score'] for slice in range(6)) -
                min(newScores[slice]['score'] for slice in range(6)))
    if newRange < oldRange:
        return newSystems, newScores
    return systems, scores


def checkMapValidity(systems):
    for location, system in enumerate(systems):
        adjacency = list(map(lambda x: systems[x], adjmap[location]))
        if system in [25, 26]:
            if (system + 15 + 2 * (25 - system)) in adjacency:
                return False
        if system in [41, 42, 43, 44, 45]:
            if any(x in adjacency for x in [41, 42, 43, 44, 45]):
                return False
    return True


def generateGalaxy():
    systems = []
    
    systems = sample(tiles, 30)
    while not checkMapValidity(systems):
        systems = sample(tiles, 30)
    
    scores = scoreGalaxy(systems)
    return systems, scores


def generateBalancedGalaxy(balancingfactor = 2000):
    x = 0
    systems, scores = generateGalaxy()
    while x < balancingfactor:
        system, scores = balanceGalaxy(systems, scores)
        if checkMapValidity(systems):
            x += 1
    return [str(x) for x in systems]