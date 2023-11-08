from Script.objetos_abstratos.animacao import Animacao
from Script.gerenciadores.clock import Clock
from Script.grid import Grid
from Script.icones.icon import Icon
import pygame, numpy as np

clockBag = Clock()
class Bag(Animacao):
    def __init__(self, sprites, proporcoes, priorityArray, mouse, allMessage, position: tuple[int, int], key_sprites="", *groups) -> None:
        super().__init__(sprites, position, key_sprites,*groups)
        self.mouse = mouse
        self.proporcoes = proporcoes
        self.display = pygame.display.get_surface()
        self.allBagGroups = priorityArray
        self.pockets = self.allBagGroups.createGroup(priority=1)
        self.slots = self.allBagGroups.createGroup(priority=2)
        self.grid = Grid(self.proporcoes, self.display, 'Data/Exel/mapa.xlsx')
        self.timer = clockBag.createTimer(manage=False)
        self.allMessage = allMessage

        self.storage = np.array([])
        self.slotActivated = None
        self.returnDescarte = False
        self.open = False
        self.abrindo = False
        self.speed = 0.4
        self.loadingBag()

    def loadingBag(self):
        posy = self.rect.centery - int(10 * self.proporcoes.y)
        self.sprites['bolso_invertido'] = np.array([pygame.transform.flip(sprite, True, False) 
                            for sprite in self.sprites['bolso_lateral']])

        self.bolsol = self.Pocket(0, self.grid, self.mouse, self.sprites, self.allBagGroups, (-50, -50), key_sprites='bolso_lateral')
        self.bolsol.rect.centery = posy
        self.bolsol.rect.right = self.rect.left
        self.bolsol.loading()
        for slot in self.bolsol.slots:
            slot.rect.x += int(8 * self.proporcoes.x)

        self.bolsor = self.Pocket(1, self.grid, self.mouse, self.sprites, self.allBagGroups, (-50, -50), key_sprites='bolso_invertido')
        self.bolsor.rect.centery = posy
        self.bolsor.rect.left = self.rect.right
        self.bolsor.loading()
        
        self.pockets.add(self.bolsol, self.bolsor)
        self.slots.exibir = False
        self.loadingSlot(0)
    
    def loadingSlot(self, levelLoad):
        def verificacao(tag):
            for obj in tag.split(' '):
                if 'l' in obj[0]: return int(obj[1:])

        tags, positios = self.grid.queryObject('slot', 'Bag', 80)
        for tag, pos in zip(tags, positios):
            levelSlot = verificacao(tag); x, y = pos
            if levelSlot == levelLoad:
                self.Slot(len(self.storage), self.sprites, self.allBagGroups, clockBag.createTimer(manage=False),
                self.pos_relative(x, y), 'slot', self.slots)
                self.storage = np.append(self.storage, 0)

    def pos_relative(self, x, y):
        return (x+self.rect.x, y+self.rect.y)
    
    def open_close(self):
        self.abrindo = False if self.abrindo else True
        self.open = True

    def returnIndexSlot(self, condiction=0):
        return np.where(self.storage == condiction)[0]

    def add(self, item, grupoRemocao):
        indexSlot = self.returnIndexSlot()
        if indexSlot.size:
            slotAlvo = self.slots.sprites()[indexSlot[0]]
            self.storage[indexSlot[0]] = 1
            item.modifySizeInSlot()
            slotAlvo.item.add(item); grupoRemocao.remove(item)
            return True
        self.allMessage.createMessage('Inventário lotado') # ~~~~~~ Aviso de inventário cheio
        return False
    
    def descartar(self, perimetroDescarte, pdp, reference=False):
        if self.slotActivated and self.discard:
            residuo = self.slotActivated.item.sprite
            if residuo:
                if residuo.type == perimetroDescarte.type:
                    pdp.ganhar_pdp(reference if reference else self.mouse.image, residuo.valor)
                else: pdp.perder_pdp(reference if reference else self.mouse.image, residuo.valor)
                self.slotActivated.item.remove(self.slotActivated.item)
                self.storage[self.slotActivated.id] = 0
                perimetroDescarte.index_sprites = 8
    
    def trocar(self, slot1, slot2):
        item = slot1.item.sprite
        slot1.item.add(slot2.item.sprite)
        slot2.item.add(item)
        slot1.reset(); slot2.reset()
        self.slotActivated = None

    def mover(self, slotSaida, slotEntrada):
        slotEntrada.item.add(slotSaida.item.sprite)
        slotSaida.item.remove(slotSaida.item)
        slotEntrada.reset(); slotSaida.reset()
        self.storage[slotSaida.id] = 0
        self.storage[slotEntrada.id] = 1
        self.slotActivated = None
    
    def removeInteraction(self):
        if self.slotActivated: self.slotActivated.reset()
        self.slotActivated = None
    
    # ~~~~~ Interação
    def interaction(self, slot, colisao, grupoSlot, delta):
        grupoSlot.update(slot, colisao, delta)
        self.discard = False

        if slot and colisao:
            slot = slot[0]
            if self.mouse.botaoL:
                slot.activated = True
                slot.index_sprites = 1
            self.timer.restart()

            if self.slotActivated == None:
                if slot.activated: self.slotActivated = slot
            else:
                if self.slotActivated.item:
                    if slot != self.slotActivated:
                        self.slotActivated.interaction = True
                        slot.interaction = True

                        if slot.activated:
                            if slot.slotPocket:
                                if slot.item:...
                            elif slot.item: self.trocar(self.slotActivated, slot)
                            else: self.mover(self.slotActivated, slot)
                        if self.mouse.botaoR: self.removeInteraction(); slot.reset()
                    else:
                        self.discard = True
                        if self.mouse.botaoR or self.mouse.botaoL:
                            if self.slotActivated.item:... # ~~~~~~ Mensagem: Fora do alcance das lixeiras
                            self.removeInteraction()
                else:
                    if self.mouse.botaoL or self.mouse.botaoR: self.removeInteraction()
        else:
            if self.slotActivated:
                if self.slotActivated.key_sprites != 'slot_vazio':
                    self.timer.countdown(0.5)
                    if self.timer.finished: self.removeInteraction()
                else: self.removeInteraction()
                if self.mouse.botaoL or self.mouse.botaoR: self.removeInteraction()
    
    # ~~~~~ Update Bag
    def update(self, delta, keyboard) -> None:
        self.returnIndexSlot()
        velocidade = self.speed * delta

        if keyboard.event(pygame.K_TAB): self.open_close()
        if keyboard.event(pygame.K_ESCAPE): self.abrindo = False
        if self.open:
            self.updateImage()
            if self.abrindo:
                self.speed = 0.35
                if self.index_sprites >= self.rangeSprites:
                    self.index_sprites = self.rangeSprites

                    # ~~ slots
                    self.slots.exibir = True
                    slot = self.mouse.collideImg(self.slots)
                    collideSlot = self.mouse.collideObj(self.slots)
                    self.interaction(slot, collideSlot, self.slots, delta)

                    # ~~ pockets
                    bolso = self.mouse.collideImg(self.pockets)
                    self.pockets.update(bolso, self.mouse.collideObj(self.pockets), delta)
                else:
                    self.discard = False
                    self.slotActivated = None
                    self.index_sprites += velocidade
            else:
                self.speed = 0.55
                self.slots.exibir = False
                self.slotActivated = None
                self.slots.update(False, False, delta, bagClose=True)
                if self.index_sprites <= -1:
                    self.index_sprites = -1
                    self.open = False
                else: self.index_sprites -= velocidade
                self.pockets.update(False, False, delta)
    
    class Pocket(Animacao):
        def __init__(self, id, grid, mouse, sprites, allbagGroups, position: tuple[int, int], key_sprites="", *group) -> None:
            super().__init__(sprites, position, key_sprites, *group)
            self.display = pygame.display.get_surface()
            self.mouse = mouse
            self.grid = grid
            self.allBagGroups = allbagGroups
            self.slots = self.allBagGroups.createGroup(priority=2)
            self.slots.exibir = False
            self.estado = False
            self.speed = 0.4
            self.id = id
        
        def pos_relative(self, x, y):
            return (x+self.rect.x, y+self.rect.y)

        def loading(self):
            contador = 0
            for x, y in self.grid.queryObject('slot', 'Pocket', 80)[1]:
                slot = Bag.Slot(contador, self.sprites, self.allBagGroups, clockBag.createTimer(manage=False),
                                self.pos_relative(x, y), 'slot', self.slots)
                slot.slotPocket = True
                contador += 1

        def update(self, estado, collisionRect, delta) -> None:
            def fechar():
                self.speed = 0.55
                if self.index_sprites <= 0: self.index_sprites = 0
                else: self.index_sprites -= velocidade

            velocidade = self.speed * delta
            self.estado = estado
            self.updateImage()

            if self.estado and collisionRect:
                self.speed = 0.35
                if self.estado[0].id == self.id:
                    if self.index_sprites >= self.rangeSprites:
                        self.index_sprites = self.rangeSprites
                        self.slots.exibir = True
                        slot = self.mouse.collideImg(self.slots) 
                        self.slots.update(slot, self.mouse.collideObj(self.slots), delta)
                    else: self.index_sprites += velocidade
                else: fechar()
            else: 
                self.slots.exibir = False; fechar()
                self.slots.update(False, False, delta, bagClose=True)
            
    class Slot(Animacao):
        def __init__(self, id, sprites, allBagGroups, timer, position: tuple[int, int], key_sprites="", *group) -> None:
            super().__init__(sprites, position, key_sprites, *group)
            self.id = id
            self.item = allBagGroups.createGroupSingle(priority=3); self.item.exibir = False
            self.simbolo = allBagGroups.createGroupSingle(priority=4); self.simbolo.exibir = False
            self.icon = Icon(self.sprites['acoes_slot'], self.rect.center, self.simbolo); self.icon.alpha = 0
            self.group = group[0]
            self.timer = timer

            self.slotPocket = False
            self.activated = False
            self.interaction = False
            self.speed = 0.3

        def keyVerification(self):
            if self.key_sprites == 'slot': self.index_sprites = 0
            if self.item: self.key_sprites = f'slot_{self.item.sprite.type}'
            else: self.key_sprites = 'slot_vazio'

        def animation(self, delta):
            if not self.slotPocket:
                velocidade = self.speed * delta
                self.timer.countdown(0.15)
                if self.timer.finished:
                    self.keyVerification(); self.icon.enterAlpha(delta)
                    self.simbolo.exibir = True; self.icon.index = 2
                    if self.index_sprites >= self.rangeSprites:
                        self.index_sprites = self.rangeSprites
                    else: self.index_sprites += velocidade
        
        def reset(self):
            self.simbolo.exibir = False
            self.activated = False
            self.interaction = False
            self.icon.alpha = 0
            self.index_sprites = 0
            self.key_sprites = 'slot'

        def update(self, slot, colisaoRect, delta, bagClose=False) -> None:
            self.item.exibir = self.group.exibir
            self.rangeSprites = len(self.sprites[self.key_sprites]) - 1
            self.image = self.sprites[self.key_sprites][int(self.index_sprites)]

            if bagClose: self.reset()
            if self.item: self.item.sprite.rect.center = self.rect.center
            if self.interaction:
                self.interaction = False
                if slot:
                    if slot[0].id == self.id: self.icon.index = 0
                    else: self.icon.index = 1
                self.simbolo.exibir = True
                self.key_sprites = 'slot'
                self.index_sprites = 2
                self.icon.enterAlpha(delta)
                self.timer.restart()
            else:
                if not self.activated:
                    if slot and colisaoRect:
                        if slot[0].id == self.id:
                            self.index_sprites = 1
                        else: self.reset()
                    else: self.reset()
                else: self.animation(delta)
