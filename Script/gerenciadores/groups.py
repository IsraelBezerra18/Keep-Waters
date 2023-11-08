from Script.geometry import distCollide
import pygame, numpy as np

class Group(pygame.sprite.Group):
    def __init__(self, priority=0) -> None:
        super().__init__()
        self.exibir = True
        self.__priority = priority
    
    @property
    def size(self):
        return len(self)

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, priority):
        self.__priority = priority

class GroupSingle(pygame.sprite.GroupSingle):
    def __init__(self, priority=0) -> None:
        super().__init__()
        self.exibir = True
        self.__priority = priority
    
    @property
    def size(self):
        return len(self)

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, priority):
        self.__priority = priority

class PriorityArray:
    '''Armazena e desenha grupos na ordem de prioridade, sendo o primeiro 
    grupo a ser desenhado na tela o grupo de prioridade=0.'''
    def __init__(self) -> None:
        self.array = np.array([])
        self.invisible = None

    def draw(self, display):
        for grupo in self.array:
            if grupo.exibir and grupo.priority != self.invisible:
                grupo.draw(display)
    
    def remove(self, group):
        index = np.where(self.array == group)[0][0]
        self.array = np.delete(self.array, index)
    
    def createGroup(self, priority: int):
        grupo = Group(priority)
        self.array = np.append(self.array, [grupo])
        self.sorted()
        return grupo
    
    def createGroupSingle(self, priority: int):
        grupo = GroupSingle(priority)
        self.array = np.append(self.array, [grupo])
        self.sorted()
        return grupo

    def get_obj(self, priority: int):
        return self.array[priority]

    def not_draw(self, priority=None):
        self.invisible = priority

    def sorted(self):
        self.array = np.array(sorted(self.array, key=lambda group: group.priority))

class GroupingManager:
    '''Gerencia uma matriz de grupos sprite.'''
    def __init__(self) -> None:
        self.array = np.array([])
    
    @property
    def lengthRow(self):
        return len(self.array)
    
    @property
    def lengthCol(self):
        return len(self.array[0]) if self.array.size else 0

    def collide(self, objRef):
        collide = []
        for group in self.array:
            identify = pygame.sprite.spritecollide(objRef, group, False)
            collide.extend(distCollide(objRef, identify, dist=65))
        return collide
    
    def return_all(self):
        return np.array([sprite for group in self.array for sprite in group])

    def queryObj(self, row, col):
        if 0 <= row <= self.lengthRow-1:
            grupo = self.array[row]
            if 0 <= col <= self.lengthCol-1:
                return grupo.sprites()[col]
        return False

    def createLine(self):
        group = Group()
        self.array = np.append(self.array, group)
        return group

    def update(self, *arg):
        for group in self.array:
            group.update(*arg)
