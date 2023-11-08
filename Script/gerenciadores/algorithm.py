from Script.gerenciadores.groups import GroupingManager
from Script.geometry import getDist
from collections import deque
import numpy as np, pygame

verde = (0, 255, 0)
vermelho = (255, 0, 0)
azul = (0, 0, 255)
    
class VisionField:
    def __init__(self, mapa, radius: int, sizeBlock: int, proporcoes: pygame.math.Vector2) -> None:
        '''Algoritmo de mapeamento e busca em largura guiada.'''
        # ~~ Mapeamento
        self.proporcoes = proporcoes
        self.sizeBlockX = int(sizeBlock * self.proporcoes.x)
        self.sizeBlockY = int(sizeBlock * self.proporcoes.y)
        self.radius = int(radius * self.proporcoes.x)
        self.gridField = GroupingManager()
        self.mapa = mapa

        # ~~ Busca
        self.parent = {} # dicionário de caminhos
        self.cost = {} # dicionário de custo

    class Block(pygame.sprite.Sprite):
        '''Objeto referente as unidades que compoem a grade.'''
        def __init__(self, x, y, largura, altura, *groups) -> None:
            super().__init__(*groups)
            self.blockedFixed = False
            self.status = False
            self.rect = pygame.Rect(x, y, largura, altura)
            self.posMap = pygame.Vector2(x, y)
            self.color = vermelho
        
        @property
        def blocked(self):
            return self.status
        
        @blocked.setter
        def blocked(self, value: bool):
            self.status = value
        
        def update(self, mapa):
            self.rect.center = mapa.get_posRect(self.posMap)
            self.status = False if not self.blockedFixed else True

        def draw(self, display):
            pygame.draw.rect(display, self.color, self.rect, width=3, border_radius=15)

        def drawLivre(self, display):
            pygame.draw.rect(display, verde, self.rect, width=3, border_radius=15)
    
    def draw_path(self, display, obj, path):
        if path:
            posX, posY = self.gridIdentify(obj.posMap.xy)
            blockAtual = self.gridField.queryObj(posY, posX)
            blockAtual.drawLivre(display)
            for block in path:
                block.drawLivre(display)

    def draw_perim(self, display):
        blocks = self.gridField.return_all()
        identify = np.where(np.array([block.blocked for block in blocks]))[0]
        for pos in identify:
            blocks[pos].draw(display)
        pygame.draw.circle(display, verde, self.mapa.get_posRect(self.posMap), self.radius, 5)
    
    def gridIdentify(self, pos):
        '''Identifica as coordenadas de um bloco na grid a partir da posição de um ponto.'''
        return (int(getDist((pos[0], 0), ((self.posMap.x - self.radius), 0)) / self.sizeBlockX), 
                int(getDist((0, pos[1]), (0, (self.posMap.y - self.radius))) / self.sizeBlockY))

    def loadingGrid(self, center: tuple[int, int], radius=False):
        '''Realiza o mapeamento da área em um raio definido.'''
        centerx = int(center[0] * self.proporcoes.x)
        centery = int(center[1] * self.proporcoes.y)
        self.posMap = pygame.Vector2(centerx, centery)
        self.radius = int(radius * self.proporcoes.x) if radius else self.radius
        posBlock = self.mapa.grid.positiosBlock
        for y in range(centery - self.radius, centery + self.radius + 1, self.sizeBlockY):
            line = self.gridField.createLine()
            for x in range(centerx - self.radius, centerx + self.radius + 1, self.sizeBlockX):
                blockGrid = self.Block(x, y, self.sizeBlockX, self.sizeBlockY)
                blockGrid.update(self.mapa)
                if getDist((centerx, centery), blockGrid.rect.center) < self.radius:
                    colision = np.where(
                        (x - self.sizeBlockX <= posBlock[:, 0]) & 
                        (posBlock[:, 0] <= x + self.sizeBlockX) &
                        (y - self.sizeBlockY <= posBlock[:, 1]) & 
                        (posBlock[:, 1] <= y + self.sizeBlockY)
                    )[0]
                    if colision.size: blockGrid.blockedFixed = True
                else: blockGrid.blockedFixed = True
                line.add(blockGrid)

    def fieldUpdate(self, *groupsColision):
        '''Atualiza a grade quando objetos entram no campo de visão'''
        identify = np.array([sprite for group in groupsColision for sprite in group])
        positios = np.array([(int(sprite.posMap.x), (sprite.posMap.y)) for sprite in identify])
        inField = np.where(getDist(*positios, self.posMap.xy) <= self.radius)[0]
        self.gridField.update(self.mapa)

        for pos in inField:
            colision = self.gridField.collide(identify[pos])
            for block in colision:
                block.blocked = True

    def pathValidation(self, block):
        '''Verifica se o valor na célula não é bloqueado.'''
        return not block.blocked

    def createPath(self, posInitial: tuple[int, int], posFinal: tuple[int, int]):
        '''Gera uma lista contendo o caminho até o ponto especificado.'''

        def reverse(pos: tuple):
            num1, num2 = pos
            return num2, num1

        startRow, startCol = reverse(self.gridIdentify(posInitial))
        finalRow, finalCol = reverse(self.gridIdentify(posFinal))

        blockInit = self.gridField.queryObj(startRow, startCol)
        blockFinal = self.gridField.queryObj(finalRow, finalCol)

        if blockInit and blockFinal and not blockInit.blocked and not blockFinal.blocked:

            self.queue = deque([(startRow, startCol)])
            self.parent = {}
            self.cost = {}
            self.cost[(startRow, startCol)] = 0

            while self.queue:
                # Ordena a lista com base na heurística
                self.queue = deque(sorted(self.queue, key=lambda pos: getDist(pos, (finalRow, finalCol)) + self.cost.get(pos, float('inf'))))
                row, col = self.queue.popleft()

                # ~~ Chegou ao destino
                if (row, col) == (finalRow, finalCol):
                    path = []
                    current = (finalRow, finalCol)
                    while current != (startRow, startCol):
                        path.append(self.gridField.queryObj(*current))
                        current = self.parent[current]
                    path.append(self.gridField.queryObj(startRow, startCol))
                    path.reverse()
                    return path
                
                # ~~ Busca heurística em largura
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    newRow, newCol = row + dr, col + dc
                    newPos = (newRow, newCol)

                    if (
                        0 <= newRow <= self.gridField.lengthRow and 0 <= newCol <= self.gridField.lengthCol
                        and self.pathValidation(self.gridField.queryObj(newRow, newCol))
                    ):
                        distCust = 1 # Custo da distância entre um nó e outro
                        if newPos not in self.cost or (self.cost.get((row, col), 0) + distCust) < self.cost.get(newPos, float('inf')):
                            self.cost[newPos] = self.cost.get((row, col), 0) + distCust
                            self.queue.append(newPos)
                            self.parent[newPos] = (row, col)

        return None # ~~ Caminho não encontrado
