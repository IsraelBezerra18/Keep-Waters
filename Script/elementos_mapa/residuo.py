import pygame, random, numpy as np
from Script.objetos_abstratos.animacao import Animacao
from Script.gerenciadores.text import TextManager
from Script.geometry import interactCollide


class ResiduoInMap:
    def __init__(self, sprites, mapa, allGroups, proporcoes) -> None:
        self.sprites = sprites
        self.mapa = mapa
        self.residuosMap = allGroups.createGroup(priority=1)
        self.proporcoes = proporcoes
        self.allText = TextManager(self.proporcoes)
        self.quantResiduo = 1
    
    def sortResiduo(self):
        categorias = np.array(['metal', 'papel', 'plastico', 'vidro'])
        tipo = random.choice(categorias)
        possibilidades = np.array([key for key in self.sprites if tipo in key and not 'danificado' in key])
        escolhido = random.choice(possibilidades)
        return tipo, escolhido

    def createResiduoAreia(self, posMap):
        tipo, aparencia = self.sortResiduo()
        aparencia += '_danificado'
        self.Residuo(self.quantResiduo, tipo, self.sprites, (posMap.x, posMap.y), aparencia, self.residuosMap)
        self.quantResiduo += 1
    
    def update(self, keyboard, delta):
        player = self.mapa.ref
        if not player.objBag.open:
            colisao = pygame.sprite.spritecollide(player, self.residuosMap, False)
            colisao = interactCollide(player, colisao, int(70 * self.proporcoes.x))
            if colisao:
                self.residuosMap.update(colisao.id, self.mapa, delta)
                if keyboard.event(pygame.K_e): # ~~~~~~~~ Coleta
                    if player.bag.sprite.add(colisao, self.residuosMap):
                        player.interaction = True
                        player.index_sprites = 0
            else: self.residuosMap.update(False, self.mapa, delta)

    class Residuo(Animacao):
        def __init__(self, id, type, sprites, posMap, key_sprites="", *group) -> None:
            super().__init__(sprites, posMap, key_sprites, *group)
            self.id = id
            self.type = type
            self.sprites = sprites
            self.posMap = pygame.math.Vector2(posMap[0], posMap[1])
            self.speed = 1

            match self.type:
                case 'metal': self.valor = 40
                case 'vidro': self.valor = 30
                case 'plastico': self.valor = 20
                case 'papel': self.valor = 10

        def modifySizeInSlot(self):
            self.key_sprites += '_slot'
            self.index_sprites = 0
            self.image = self.sprites[self.key_sprites][int(self.index_sprites)]
            self.rect = self.image.get_rect()
        
        def modifySizeInMap(self):
            self.key_sprites = self.key_sprites.replace('_slot', '')
            self.index_sprites = 0
            self.image = self.sprites[self.key_sprites][int(self.index_sprites)]
            self.rect = self.image.get_rect()

        def animation(self, delta):
            velocidade = self.speed * delta
            if self.index_sprites >= self.rangeSprites:
                self.index_sprites = self.rangeSprites
            else: self.index_sprites += velocidade
            
        def update(self, idCollide, mapa, delta) -> None:
            self.updateImage()
            if idCollide and idCollide == self.id:
                self.animation(delta)
            else: self.index_sprites = 0
            self.rect.center = mapa.get_posRect(self.posMap)
