from Script.icones.icon import Icon, IconMoveRect, IconMoveinMap
from Script.gerenciadores.groups import PriorityArray
import pygame

class Pdp:
    def __init__(self, sprites, clock, textManager, proporcoes) -> None:
        self.__pdp = 0
        self.display = pygame.display.get_surface()
        self.rectDisplay = self.display.get_rect()
        self.proporcoes = proporcoes
        self.sprites = sprites
        self.clock = clock
        self.allText = textManager
        self.allGroups = PriorityArray()

        posPDP = (self.rectDisplay.left + int(35 * self.proporcoes.x), self.rectDisplay.top + int(60 * self.proporcoes.y))
        self.image_pdp = self.allGroups.createGroupSingle(priority=0); self.image_pdp.add(
            Icon(self.sprites['pdp'], posPDP))
        self.setas = self.allGroups.createGroup(priority=1)
        self.valores = self.allGroups.createGroup(priority=1)
        self.sizeText = 18
        self.textPDP = self.allText.createText(str(self.__pdp), self.sizeText, (-10, -10))

    @property
    def value(self):
        return self.__pdp

    def ganhar_pdp(self, obj_ref, valor):
        self.setas.add(IconMoveinMap(self.sprites['ganho'], obj_ref, self.proporcoes, self.clock.createTimer()))
        texto = self.allText.createText(f'+{valor}', self.sizeText, self.posText, color=(153, 229, 80), manager=False)
        self.valores.add(IconMoveRect(texto.image, texto.pos, self.proporcoes, self.clock.createTimer()))
        self.__pdp += valor
        self.textPDP.set_text(str(self.__pdp))
    
    def perder_pdp(self, obj_ref, valor):
        self.setas.add(IconMoveinMap(self.sprites['perca'], obj_ref, self.proporcoes, self.clock.createTimer()))
        texto = self.allText.createText(f'-{valor}', self.sizeText, self.posText, color=(222, 66, 66), manager=False)
        self.valores.add(IconMoveRect(texto.image, texto.pos, self.proporcoes, self.clock.createTimer()))
        verificacao = self.__pdp - valor
        if verificacao <= 0: self.__pdp = 0
        else: self.__pdp = verificacao
        self.textPDP.set_text(str(self.__pdp))

    def acao_negativa(self, obj_ref):
        self.setas.add(IconMoveinMap(self.sprites['perca'], obj_ref, self.proporcoes, self.clock.createTimer()))
    
    def update(self, mapa, delta):
        posXtextPDP = int(self.image_pdp.sprite.rect.right + 10 * self.proporcoes.x)
        self.textPDP.rect.centery = self.image_pdp.sprite.rect.centery
        self.textPDP.rect.left = posXtextPDP
        self.posText = (int(self.textPDP.rect.right + (40 * self.proporcoes.x)), self.textPDP.rect.centery)

        self.setas.update(delta)
        self.valores.update(delta)
        for seta in self.setas:
            posX, posY = mapa.get_posRect(seta.posMap)
            seta.rect.centerx = posX
            seta.rect.centery = posY
            if seta.sumir:
                self.clock.removeTimer(seta.timer)
                self.setas.remove(seta)
        for valor in self.valores:
            valor.rect.centerx = valor.pos
            if valor.sumir:
                self.clock.removeTimer(valor.timer)
                self.valores.remove(valor)
        self.allGroups.draw(mapa.display)
