from Script.objetos_abstratos.animacao import Animacao
from Script.icones.icon import Icon
from copy import copy
import pygame, numpy as np

class Hub:
    def __init__(self, bag, sprites, allGroups, proporcoes) -> None:
        self.allGroups = allGroups
        self.fundoHub = self.allGroups.createGroupSingle(priority=0)
        self.slotsPrimario = self.allGroups.createGroup(priority=1); self.slotsPrimario.exibir = False
        self.slotsSecundario = self.allGroups.createGroup(priority=1); self.slotsSecundario.exibir = False
        self.display = pygame.display.get_surface()
        self.rectDisplay = self.display.get_rect()
        self.sprites = sprites
        self.bag = bag

        self.proporcoes = proporcoes
        self.slotAlvo = None
        self.loading()

    def loading(self):
        bolsoLeft = self.bag.bolsol
        posHSlot = (int(self.rectDisplay.left + 50 * self.proporcoes.x), int(self.rectDisplay.bottom - 50 * self.proporcoes.y))
        self.pL = self.HSlot(0, self.sprites['slot_primario'], self.allGroups, posHSlot)
        self.pL.slotCopy = bolsoLeft.slots.sprites()[0]
        self.pR = self.HSlot(1, self.sprites['slot_primario'], self.allGroups, 
                             (self.pL.rect.right + 35 * self.proporcoes.x, self.pL.rect.centery))
        self.pR.slotCopy = bolsoLeft.slots.sprites()[1]
        self.slotsPrimario.add(self.pL, self.pR)

        simboloDescarte = self.bag.sprites['acoes_slot'][2]
        self.s1 = self.HSlot(0, self.sprites['slot_secundario'], self.allGroups, 
                             (self.pR.rect.right + 35 * self.proporcoes.x, self.pR.rect.centery))
        self.s1.rect.bottom = self.pR.rect.bottom
        self.s2 = self.HSlot(1, self.sprites['slot_secundario'], self.allGroups, 
                             (self.s1.rect.right + 30 * self.proporcoes.x, self.s1.rect.centery))
        self.s3 = self.HSlot(2, self.sprites['slot_secundario'], self.allGroups, 
                             (self.s2.rect.right + 30 * self.proporcoes.x, self.s2.rect.centery))
        self.s1.loading(simboloDescarte), self.s2.loading(simboloDescarte); self.s3.loading(simboloDescarte)
        self.slotsSecundario.add(self.s1, self.s2, self.s3)

        self.fundo = self.Fundo(self.sprites['fundo'], (0, 0), self.allGroups)
        self.fundo.loadIcon(self.bag.sprites['icone_bag'])
        self.fundoHub.add(self.fundo)

    def descartar(self, perimetroDescarte, player, pdp, keyboard):
        if self.slotAlvo:
            self.slotAlvo.interaction = True
            if keyboard.event(pygame.K_e):
                self.bag.discard = True
                self.bag.slotActivated = self.slotAlvo.slotCopy
                self.bag.descartar(perimetroDescarte, pdp, player)
                self.slotAlvo = None

    def animation(self, delta, reset=False):
        self.slotsPrimario.update(delta, reset)
        self.slotsSecundario.update(delta, reset)
        if reset:
            self.slotsPrimario.exibir = False
            self.slotsSecundario.exibir = False
        else:
            self.slotsPrimario.exibir = True
            self.slotsSecundario.exibir = True

    def update(self, keyboard, delta, reset=False):
        self.fundoHub.update(delta, self.rectDisplay, self.proporcoes)
        if not reset:
            self.fundo.open = True
            if self.fundo.index_sprites == self.fundo.rangeSprites:
                self.animation(delta)
                slotsBag = np.array(self.bag.slots.sprites())
                indexSlot = self.bag.returnIndexSlot(condiction=1)
                size = indexSlot.size
                if size:
                    tecla = keyboard.getkey()
                    if tecla and tecla.isdigit() and 1 <= int(tecla) <= 3:
                        self.slotAlvo = self.slotsSecundario.sprites()[int(tecla)-1]
                        if self.slotAlvo.activated:
                            self.slotAlvo.activated = False
                            self.slotAlvo = None
                        else:
                            if self.slotAlvo.item: self.slotAlvo.activated = True
                            else: self.slotAlvo = None
                    
                for index in range(3):
                    hslot = self.slotsSecundario.sprites()[index]
                    if hslot != self.slotAlvo: hslot.reset()
                    if index <= size-1:
                        newSlot = slotsBag[indexSlot[index]]
                        if hslot.residuoReference != newSlot.item.sprite:
                            hslot.item.remove(hslot.item)
                            hslot.slotCopy = newSlot
                    else: hslot.slotCopy = None
        else:
            self.fundo.open = False
            self.slotAlvo = None
            self.animation(delta, reset=True)

    class HSlot(Animacao):
        def __init__(self, id, sprites, allgroups, position: tuple[int, int], key_sprites="", *group) -> None:
            super().__init__(sprites, position, key_sprites, *group)
            self.icon = allgroups.createGroupSingle(priority=3); self.icon.exibir = False
            self.item = allgroups.createGroupSingle(priority=2)

            self.id = id
            self.slotCopy = None
            self.residuoReference = None
            
            self.activated = False
            self.interaction = False
            self.speed = 0.5

        def loading(self, iconSprite):
            self.icon.add(Icon(iconSprite, self.rect.center))
            self.icon.sprite.alpha = 0
        
        def animation(self, delta):
            velocidade = self.speed * delta
            if self.index_sprites >= self.rangeSprites:
                self.index_sprites = self.rangeSprites
            else: self.index_sprites += velocidade

        def reset(self):
            if self.icon: self.icon.sprite.alpha = 0
            self.index_sprites = 0
            self.interaction = False
            self.icon.exibir = False
            self.activated = False

        def update(self, delta, reset):
            if not reset:
                self.updateImage()
                self.item.exibir = True

                if self.slotCopy:
                    if not self.item and self.slotCopy.item:
                        self.residuoReference = self.slotCopy.item.sprite
                        copia = copy(self.residuoReference)
                        copia.modifySizeInMap()
                        copia.rect.center = self.rect.center
                        self.item.add(copia)
                else:
                    self.item.remove(self.item)
                    self.residuoReference = None

                if self.interaction:
                    self.interaction = False
                    self.icon.exibir = True
                    self.icon.sprite.enterAlpha(delta, speed=10)
                else:
                    if self.icon: self.icon.sprite.alpha = 0
                    self.icon.exibir = False

                if self.activated: self.animation(delta)
                else: self.reset()
            else:
                self.item.exibir = False
                self.reset()

    class Fundo(Animacao):
        def __init__(self, sprites, position: tuple[int, int], allGroups, key_sprites="", *group) -> None:
            super().__init__(sprites, position, key_sprites, *group)
            self.icon = allGroups.createGroupSingle(priority=2)
            self.open = False
            self.speed = 0.5
        
        def loadIcon(self, imageIcon):
            self.icon.add(Icon(imageIcon, self.rect.center))
            self.icon.sprite.alpha = 0
        
        def abrir(self, delta):
            if self.index_sprites >= self.rangeSprites:
                self.index_sprites = self.rangeSprites
                self.icon.sprite.exibir = False
                self.icon.sprite.alpha = 0
            else:
                self.icon.sprite.closeAlpha(delta)
                self.index_sprites += self.velocidade
        
        def fechar(self, delta):
            if self.index_sprites <= 0:
                self.index_sprites = 0
                self.icon.exibir = True
                self.icon.sprite.enterAlpha(delta, speed=10)
            else: self.index_sprites -= self.velocidade
        
        def update(self, delta, rectDisplay, proporcoes):
            self.updateImage()
            self.velocidade = self.speed * delta
            self.rect = self.image.get_rect()
            self.rect.bottom = int(rectDisplay.bottom - 5 * proporcoes.y)
            self.rect.x = int(rectDisplay.left + 6 * proporcoes.x)
            self.icon.sprite.rect.center = self.rect.center

            if self.open: self.abrir(delta)
            else: self.fechar(delta)
