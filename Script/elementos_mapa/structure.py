import pygame
from Script.icones.icon import Icon, IconAnimado
from Script.geometry import interactCollide
from Script.gerenciadores.groups import Group

class Structures:
    def __init__(self, sprites, mapa, allGroups, proporcoes) -> None:
        self.sprites = sprites
        self.proporcoes = proporcoes
        self.groupStructure = allGroups.createGroup(priority=3)
        self.groupElements = allGroups.createGroup(priority=4)
        self.perimetros = Group()
        self.mapa = mapa

    def createStructure(self, interface, tagStructure):
        self.mapa = self.mapa.sprite
        grid = self.mapa.grid
        tags, position = grid.queryObject('estrutura', 'Map')

        for tag, pos in zip(tags, position):
            if tagStructure in tag:
                verification = tag.split(' ')
                angle = 0
                if 'angle' in tag:
                    angle = verification[-1]
                    angle = int(angle[6:])
                colision = self.mapa.grid.typeCollide(tag)
                acao = self.mapa.grid.modifyBlock(tag)[-1]
                struture = self.Structure(self.sprites['corpo'][0], colision, acao, angle, pos)
                struture.loading(interface, self.sprites['tenda'][0], None, self.mapa, self.proporcoes)
                self.groupStructure.add(struture)
                self.groupElements.add(struture.tenda)
                self.perimetros.add(struture.perimetro)
    
    def update(self, keyboard):
        self.groupStructure.update(self.mapa)
        self.mapa.colision(self.mapa.ref, self.groupStructure, dist=145)
        colisaoPerimetro = pygame.sprite.spritecollide(self.mapa.ref, self.perimetros, False)
        verificacao = interactCollide(self.mapa.ref, colisaoPerimetro, dist=110)
        if verificacao:
            if keyboard.event(pygame.K_e):
                print('ok')
        
    class Structure(pygame.sprite.Sprite):
        def __init__(self, sprite, colision, acao, angle, posMap, *groups) -> None:
            super().__init__(*groups)
            self.angle = angle
            self.posMap = pygame.Vector2(*posMap)
            self.image = sprite
            self.image = pygame.transform.rotate(self.image, self.angle)
            self.colisao = colision
            self.acao = acao
        
        def loading(self, interface, imgTenda, spritesSimbolo, mapa, proporcoes):
            self.rect = self.image.get_rect(center=mapa.get_posRect(self.posMap))

            match self.angle:
                case 0:
                    reference = 'right'
                    referencePos = self.rect.right
                case -90:
                    reference = 'bottom'
                    referencePos = self.rect.bottom
                case 90:
                    reference = 'top'
                    referencePos = self.rect.top
                case _:
                    reference = 'left'
                    referencePos = self.rect.left

            self.tenda = Icon(imgTenda, (-30, -30))
            self.tenda.rotate(self.angle)
            if reference == 'left' or reference == 'right':
                hPerim = self.rect.height
                wPerim = int(70 * proporcoes.x)
                posYPerim = self.rect.centery
                self.tenda.rect.centery = self.rect.centery
                if reference == 'left':
                    self.tenda.rect.right = referencePos
                    posXPerim = self.rect.left - wPerim/2
                else:
                    self.tenda.rect.left = referencePos
                    posXPerim = self.rect.right + wPerim/2
            else: 
                wPerim = self.rect.width
                hPerim = int(70 * proporcoes.y)
                posXPerim = self.rect.centerx
                self.tenda.rect.centerx = self.rect.centerx
                if reference == 'top':
                    self.tenda.rect.bottom = referencePos
                    posYPerim = self.rect.top - hPerim/2
                else:
                    self.tenda.rect.top = referencePos
                    posYPerim = self.rect.bottom + hPerim/2
            posSimbolo = self.rect.center
            self.tenda.adaptPosMap(mapa.get_posMap(self.tenda.rect))

            # self.simbolo = IconAnimado(spritesSimbolo, posSimbolo)
            # self.simbolo.adaptPosMap(mapa.get_posMap(self.simbolo.rect))

            posPerim = (posXPerim, posYPerim)
            self.perimetro = self.Perimetro(self.rect.x, self.rect.y, wPerim, hPerim)
            self.perimetro.rect.center = posPerim
            self.perimetro.loading(interface, mapa)
        
        def update(self, mapa):
            self.rect = self.image.get_rect(center=mapa.get_posRect(self.posMap))
            self.tenda.rect = self.tenda.image.get_rect(center=mapa.get_posRect(self.tenda.posMap))
            # self.simbolo.rect = self.simbolo.image.get_rect(center=mapa.get_posRect(self.simbolo.posMap))
            self.perimetro.rect.centerx, self.perimetro.rect.centery = mapa.get_posRect(self.perimetro.posMap)
    
        class Perimetro(pygame.sprite.Sprite):
            def __init__(self, x, y, width, height, *groups):
                super().__init__(*groups)
                self.rect = pygame.Rect(x, y, width, height)
            
            def loading(self, interface, mapa):
                self.mapa = mapa
                self.interface = interface
                self.posMap = pygame.Vector2(*mapa.get_posMap(self.rect))
            
            def update(self):
                self.rect.centerx, self.rect.centery = self.mapa.get_posRect(self.posMap)

            def draw(self, display):
                pygame.draw.rect(display, (0, 255, 0), self.rect, 2)
