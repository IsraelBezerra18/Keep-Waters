from Script.objetos_abstratos.animacao import Animacao
from Script.interagiveis.button import BotaoIcon
from Script.grid import Grid
import pygame

dictExel = 'Data/Exel/mapa.xlsx'
audioBotao = ''

class Pause(Animacao):
    def __init__(self, sprites, position: tuple[int, int], allgroups, clock, key_sprites="", *group) -> None:
        super().__init__(sprites, position, key_sprites, *group)
        self.buttons = allgroups.createGroup(priority=1)
        self.timer = clock.createTimer(manage=False)
        self.interaction = False
        self.animation = False
        self.active = False
        self.speed = 0.5
        self.sequence = 0
    
    @property
    def paused(self):
        return self.active or self.interaction
    
    def loading(self, proporcoes, display, blur, allText):
        self.proporcoes = proporcoes
        self.display = display
        self.rectDisplay = self.display.get_rect()
        self.allText = allText
        self.blur = blur

        self.grid = Grid(self.proporcoes, self.display, dictExel)
        self.grid.set_distance(52)
        self.textPause = self.allText.createText('Pausa', size=29, pos=self.rect.center)
        self.textPause.set_alpha(0)

    def loadingButton(self, sprites):
        tags = self.grid.queryObject(objectTag='all', exelname='Pause')[0]
        posX = self.rect.centerx

        for name in tags:
            if self.buttons.size:
                rectReference = self.buttons.sprites()[-1].rect.bottom
                posY = rectReference + int(45 * self.proporcoes.y)
            else: 
                rectReference = self.sprites['expandir'][-1].get_rect(center=self.rectDisplay.center)
                posY = rectReference.top + int(105 * self.proporcoes.y)
            botao = BotaoIcon(sprites, None, (posX, posY), self.allText, name, 'expansao', 25)
            self.buttons.add(botao)

    def pausar(self):
        self.interaction = False if self.interaction else True
        self.blur.create(not self.active, pygame.display.get_surface(), desfoque=3)
    
    def updateButton(self, delta, mouse):
        if self.active and self.interaction:
            self.buttons.update(delta, mouse)
            return mouse.collideId(self.buttons)
        return False

    def update(self, delta):
        velocidade = self.speed * delta
        self.updateImage()

        self.rect = self.image.get_rect(center=self.rectDisplay.center)
        if self.key_sprites == 'abrir':
            self.textPause.rect.center = self.rect.center
        else: self.textPause.rect.top = self.rect.top + int(20 * self.proporcoes.y)

        if self.interaction:
            self.blur.apply()
            self.textPause.enterAlpha(delta, speed=15)
            if self.textPause.visible:
                if self.index_sprites >= self.rangeSprites:
                    self.index_sprites = self.rangeSprites
                    if self.key_sprites == 'abrir':
                        self.key_sprites = 'expandir'
                        self.index_sprites = 0
                        self.timer.restart()
                    else:
                        if not self.active:
                            self.timer.countdown(time=0.05)
                            for index, button in enumerate(self.buttons):
                                if index <= self.sequence:
                                    if not button.interaction:
                                        button.enter('ativacao', speed=0.9, delta=delta)
                                        button.enterAlpha(delta, speed=40)
                                    else: button.texto.enterAlpha(delta, speed=40)

                                if self.timer.finished:
                                    self.sequence += 1
                                    self.timer.restart()

                                if index == self.buttons.size-1 and button.texto.visible:
                                    self.active = True; self.animation = False
                else: self.index_sprites += velocidade
            else: self.animation = True
        else:
            if self.index_sprites <= 0:
                self.index_sprites = 0

                if self.key_sprites == 'expandir':
                    self.index_sprites = self.get_sizeKey('abrir')
                    self.key_sprites = 'abrir'
                else:
                    self.blur.remove()
                    self.textPause.closeAlpha(delta, speed=30)

                    if not self.textPause.alpha and not self.blur.unfocused:
                        self.animation = False
                        self.active = False
                        self.sequence = 0
            else:
                self.index_sprites -= velocidade
                self.animation = True
            
                for button in self.buttons:
                    button.key_sprites = 'expansao'
                    button.interaction = False
                    button.texto.set_alpha(0)
                    button.set_alpha(0)
