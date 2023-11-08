from Script.objetos_abstratos.animacao import Animacao
from Script.gerenciadores.groups import PriorityArray
from Script.gerenciadores.clock import Clock
from Script.icones.icon import Icon
import numpy as np, pygame

class MessageManager:
    def __init__(self, sprites, TextManager) -> None:
        self.sprites = sprites
        self.text = TextManager
        self.allGroups = PriorityArray()
        self.clock = Clock()

        self.info = np.array([])
        self.message = self.allGroups.createGroupSingle(priority=0)
    
    def createMessage(self, text, size=19):
        if np.where(self.info == text)[0].size < 3:
            self.info = np.append(self.info, (text, size))

    def update(self, delta, display, proporcoes):
        if self.message:
            self.allGroups.draw(display)
            self.message.update(delta, proporcoes, int(self.info.size / 2 - 1))
            if self.message.sprite.sumir:
                self.text.remove(self.message.sprite.textSizeArray.text)
                self.text.remove(self.info[0])
                self.allGroups.remove(self.message.sprite.icon)
                self.message.remove(self.message)
                self.info = self.info[2:]
        else:
            if self.info.size:
                text, size = self.info[0], int(self.info[1])
                mensagem = self.MessageInfo(self.sprites, self.clock.createTimer(), 
                                        self.allGroups, self.text, (-100, -100), key_sprites='ativacao')
                mensagem.texto = self.text.createText(text, size, mensagem.rect.center)
                mensagem.texto.set_alpha(0)
                self.message.add(mensagem)

    class MessageInterface:...

    class MessageInfo(Animacao):
        def __init__(self, sprites, timer, allGroups, allText, position: tuple[int, int], key_sprites="", *group) -> None:
            super().__init__(sprites, position, key_sprites, *group)
            self.display = pygame.display.get_surface()
            self.rectDisplay = self.display.get_rect()
            self.sumir = False
            self.exibirMensagem = False
            self.contagem = False
            self.texto = None
            self.timer = timer
            self.speed = 0.3

            self.icon = allGroups.createGroupSingle(priority=1)
            self.textSizeArray = allText.createText('', 10, self.rect.center)
            self.loading(sprites['icones'])
        
        def loading(self, spritesIcone):
            self.icon.add(Icon(spritesIcone, self.rect.center))
            self.icon.sprite.alpha = 0
            self.textSizeArray.set_alpha(0)

        def open(self, delta):
            velocidade = self.speed * delta
            if self.index_sprites >= self.rangeSprites:
                self.index_sprites = self.rangeSprites
                match self.key_sprites:
                    case 'ativacao':
                        self.key_sprites = 'expansao'
                        self.index_sprites = 0
                        self.speed = 0.4
                    case _:
                        self.exibirMensagem = True
                        self.contagem = True
            else:
                if self.key_sprites == 'ativacao': self.icon.sprite.enterAlpha(delta, speed=15)
                else: self.icon.sprite.closeAlpha(delta, speed=14)
                self.index_sprites += velocidade
        
        def close(self, delta):
            velocidade = self.speed * delta
            self.texto.exibir = False
            self.textSizeArray.exibir = False

            if self.index_sprites <= 0:
                self.index_sprites = 0
                match self.key_sprites:
                    case 'expansao':
                        self.speed = 0.3
                        self.key_sprites = 'saida'
                        self.index_sprites = len(self.sprites[self.key_sprites])-1
                    case _: self.sumir = True
            else:
                self.icon.sprite.index = 1
                if self.key_sprites == 'saida': self.icon.sprite.enterAlpha(delta, speed=15)
                self.index_sprites -= velocidade

        def update(self, delta, proporcoes, sizeArray):
            self.updateImage()
            self.rect = self.image.get_rect()
            self.rect.right = self.rectDisplay.right - int(10 * proporcoes.x)
            self.rect.centery = self.rectDisplay.bottom - int(50 * proporcoes.y)
            self.texto.rect.center = self.rect.center

            icone = self.icon.sprite
            icone.rect = icone.image.get_rect(center=self.rect.center)

            pos_trX, pos_trY = self.rect.topright
            self.textSizeArray.rect.topright = (pos_trX - int(16 * proporcoes.x), pos_trY + int(14 * proporcoes.y))
            self.textSizeArray.pos = self.textSizeArray.rect.center
            
            if self.exibirMensagem:
                if sizeArray:
                    self.textSizeArray.set_text(f'+{sizeArray}')
                    self.textSizeArray.enterAlpha(delta, speed=40)
                self.texto.enterAlpha(delta, speed=40)

            if self.contagem:
                self.timer.countdown(3)
                if self.timer.finished: self.close(delta)
            else:
                self.open(delta)
                self.timer.restart()
