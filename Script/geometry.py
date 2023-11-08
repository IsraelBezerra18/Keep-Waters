import numpy as np, pygame

def getDist(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5

def get_posImage(reference, pos):
    return (pos[0] - reference.rect.left, pos[1] - reference.rect.top)

def get_posRect(reference, vector):
    return (reference.rect.x + int(vector.x), reference.rect.y + int(vector.y))

def get_colorPixel(reference, vector):
    if vector.x < 0 or vector.x > reference.rect.width or vector.y < 0 or vector.y > reference.rect.height:
        return pygame.Color(0, 0, 0, 0)
    return reference.image.get_at((int(vector.x), int(vector.y)))

def interactCollide(reference, listCollide, dist=100):
    '''Retorna o objeto mais próximo dentro da distância definida.'''
    if listCollide:
        listCollide = np.array(listCollide)
        if listCollide.size > 1:
            allDist = np.array([getDist(reference.rect.center, obj.rect.center) for obj in listCollide])
            index = np.where(allDist == np.min(allDist))[0][0]
            objCollide = listCollide[index]; distCollide = allDist[index]
            if distCollide <= dist: return objCollide
        objCollide = listCollide[0]; distCollide = getDist(objCollide.rect.center, reference.rect.center)
        if distCollide <= dist: return objCollide
    return False

def distCollide(reference, listCollide, dist=100):
    '''Retorna todos os objetos dentro da distância definida'''
    collide = []
    if listCollide:
        listCollide = np.array(listCollide)
        if listCollide.size > 1:
            allDist = np.array([getDist(reference.rect.center, obj.rect.center) for obj in listCollide])
            index = np.where(allDist <= dist)[0]
            for pos in index:
                collide.append(listCollide[pos])
        else:
            objCollide = listCollide[0]; distCollide = getDist(objCollide.rect.center, reference.rect.center)
            if distCollide <= dist: collide.append(objCollide)
    return collide
