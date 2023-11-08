import numpy as np, pandas as pd, pygame
from Script.gerenciadores.groups import Group

class Grid():
    def __init__(self, proporcoes, display, directory: str) -> None:
        self.maping: None
        self.directory = directory
        self.proporcoes = proporcoes
        self.distanceX = 64
        self.distanceY = 64
        self.invibleBarrierList = Group()
        self.display = display
    
    @staticmethod
    def typeCollide(tag):
        verificacao = tag.split(' ')
        ct, cb, cl, cr = False, False, False, False
        for item in verificacao:
            if 'allc' in item: ct, cb, cl, cr = True, True, True, True
            elif 'ct' in item: ct = True # Top
            elif 'cb' in item: cb = True # Bottom
            elif 'cl' in item: cl = True # Left
            elif 'cr' in item: cr = True # Right
        return (ct, cb, cl, cr)

    def modifyPos(self, tag, x, y):
        verificacao = tag.split(' ')
        for item in verificacao:
            if 'x' in item[0]: x += int(item[1:]) * self.proporcoes.x
            elif 'y' in item[0]: y += int(item[1:]) * self.proporcoes.y
        return (int(x), int(y))
    
    def modifyBlock(self, tag):
        verificacao = tag.split(' ')
        w, h = 0, 0; acao = True
        for item in verificacao:
            if 'sa' in item: acao = False # Sem animação de colisão
            elif 'w' in item: w += int(item[1:]) * self.proporcoes.x # Largura
            elif 'h' in item: h += int(item[1:]) * self.proporcoes.y # Altura
        return (int(w), int(h), acao)

    def set_distance(self, distance: int):
        self.distanceX = distance
        self.distanceY = distance

    def update(self, mapa):
        if not mapa.ref.objBag.open:
            self.invibleBarrierList.update(mapa, self.proporcoes.x)
            mapa.colision(mapa.ref, self.invibleBarrierList)

    def queryObject(self, objectTag, exelname, distance=-1) -> np.array:
        self.distance_gridX = self.distanceX * self.proporcoes.x if distance < 0 else distance * self.proporcoes.x
        self.distance_gridY = self.distanceY * self.proporcoes.y if distance < 0 else distance * self.proporcoes.y
        self.maping = pd.read_excel(self.directory, sheet_name=exelname)
        positios = []; tags = []
        for y, linha in enumerate(self.maping.values):
            for x, tag in enumerate(linha):
                posx = int(x * self.distance_gridX); posy = int(y * self.distance_gridY)
                if isinstance(tag, str):
                    if objectTag == 'all' or objectTag in tag:
                        positios.append(self.modifyPos(tag, posx, posy))
                        tags.append(tag)
        return np.array(tags), np.array(positios)

    def invibleBarrier(self, size:tuple[int]):
        sizeX = int(size[0] * self.proporcoes.x)
        sizeY = int(size[1] * self.proporcoes.y)
        tags, positios = self.queryObject("block", "Map")
        self.positiosBlock = positios
        for tag, pos in zip(tags, positios):
            w, h, acao = self.modifyBlock(tag)
            self.invibleBarrierList.add(self.Block(pos, sizeX+w, sizeY+h, 
                                            self.typeCollide(tag), acao, self.display))
    
    class Block(pygame.sprite.Sprite):
        def __init__(self, pos, size1, size2, typeColision, acao, display, *group) -> None:
            super().__init__(group)
            self.posMap = pygame.math.Vector2(pos[0], pos[1])
            self.display = display
            self.rect = pygame.Rect(-30, -30, size1, size2)
            self.acao = acao
            self.colisao = typeColision

        def update(self, mapa, proporcao) -> None:
            self.ajust(mapa)
            # self.draw(proporcao)
        
        def draw(self, proporcao, color=(0, 255, 0)):
            if color: self.color = color
            pygame.draw.rect(self.display, color, self.rect, int(2 * proporcao))

        def ajust(self, mapa):
            self.rect.x, self.rect.y = mapa.get_posRect(self.posMap)


# ~~ Sistema de mapeamento
# [
#     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
# ]

list_bottom_keys = ["Jogar", "Tutorial", "Conquistas", "Configurações", "Créditos", "Sair do jogo"]

interface = np.array([
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "Jogar", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "Tutorial", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "Conquistas", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "Configurações", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "Créditos", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "Sair do jogo", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
])
