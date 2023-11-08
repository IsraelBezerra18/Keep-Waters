from Script.gerenciadores.groups import PriorityArray
from Script.objetos_abstratos.animacao import Animacao
from Script.gerenciadores.text import TextManager
from Script.icones.icon import Icon, IconAnimado
from Script.reprodutores.audio import Audio
import pygame

audioButton = ''
class BoxInfo:
    def __init__(self, sprites_box, mouse, proporcoes) -> None:
        self.allBox = PriorityArray()
        self.spritesBox = sprites_box
        self.proporcoes = proporcoes
        self.text = TextManager(self.proporcoes)
        self.boxAnimation = self.allBox.createGroup(priority=1)
        self.boxSolid = self.allBox.createGroup(priority=1)
        self.mouse = mouse
    
    def createBoxAnimation(self, icone, timer, audio):
        leitura = len(self.boxAnimation)
        posicaoX = (int(10 * self.proporcoes.x))
        if leitura: 
            rectBoxAnt = self.boxAnimation.sprites()[-1].rect
            posicaoY = rectBoxAnt.bottom + int(5 * self.proporcoes.y)
        else: posicaoY = int(100 * self.proporcoes.y)
        box = self.Box(self.spritesBox, self.mouse, self.proporcoes, self.allBox, self.text, (-200, -200))
        box.rect.left = posicaoX; box.rect.top = posicaoY
        box.loading(icone, timer, audio)
        box.boxOpen = True
        self.boxAnimation.add(box)

    def createBoxSolid(self, pos: tuple[int, int], reference=False):
        pos = (pos[0] * self.proporcoes.x, pos[1] * self.proporcoes.y)
        icone = Icon(self.spritesBox['box'], pos)
        if reference:
            match reference:
                case 'topleft': icone.rect.topleft = pos
                case 'topright': icone.rect.topright = pos
        self.boxSolid.add(icone)

    def update(self, display, delta):
        self.allBox.draw(display)
        self.text.blit(display)
        self.boxAnimation.update(delta)
        for index, box in enumerate(self.boxAnimation):
            if index:
                rectBoxAnt = self.boxAnimation.sprites()[index-1].rect
                box.posicaoY = rectBoxAnt.bottom + int(5 * self.proporcoes.y)
            else: box.posicaoY = int(100 * self.proporcoes.y)
            if box.sair:
                self.allBox.remove(box.icon)
                self.allBox.remove(box.iconAnimation)
                self.text.remove(box.textBox.text)
                self.boxAnimation.remove(box)
                break

    class Box(Animacao):
        def __init__(self, sprites, mouse, proporcoes, allGroups, text, position: tuple[int, int], key_sprites="box_animation", *group) -> None:
            super().__init__(sprites, position, key_sprites, *group)
            self.sair = False
            self.icon = allGroups.createGroupSingle(priority=1)
            self.iconAnimation = allGroups.createGroupSingle(priority=1); self.iconAnimation.exibir = False
            self.textBox = text.createText('', 18, self.rect.center); self.textBox.alpha = 0
            self.proporcoes = proporcoes

            self.speed = 0.4
            self.posicaoY = None
            self.redutivel = True
            self.interaction = False
            self.boxOpen = False
            self.mouse = mouse
        
        def loading(self, iconeExibicao, timer, audio):
            self.icon.add(iconeExibicao)
            rectIcone = self.icon.sprite.rect
            posIconAnimado = (rectIcone.right + int(10 * self.proporcoes.x), rectIcone.centery)
            self.iconAnimation.add(IconAnimado(self.sprites['seta'], posIconAnimado))
            self.timer = timer
            self.audio = audio
        
        def notification(self):... # ~~ Exibição de um icone quando houver atualizações relevantes na box

        def open(self, delta):
            velocidade = self.speed * delta
            if self.index_sprites >= self.rangeSprites-1:
                self.index_sprites = self.rangeSprites
                if self.key_sprites == 'box_animation':
                    self.key_sprites = 'open'
                    self.index_sprites = 0
                else:
                    self.iconAnimation.exibir = True
                    self.interaction = True
            else: self.index_sprites += velocidade

        def close(self, delta):
            velocidade = self.speed * delta
            self.interaction = False
            self.textBox.set_alpha(0)
            self.iconAnimation.sprite.close(delta, speed=2)
            if self.iconAnimation.sprite.index == 0:
                self.iconAnimation.exibir = False

            if self.index_sprites <= 0:
                self.index_sprites = 0
                if self.key_sprites == 'open':
                    self.key_sprites = 'box_animation'
                    self.index_sprites = len(self.sprites['box_animation'])-1
            else: self.index_sprites -= velocidade
        
        def mov(self, delta):
            if self.posicaoY and self.rect.top != self.posicaoY:
                velocidade = (10 * self.proporcoes.y) * delta
                dist = int(5 * self.proporcoes.y)
                if self.rect.top > self.posicaoY:
                    if self.rect.top - self.posicaoY <= dist:
                        self.rect.top = self.posicaoY
                    else: self.rect.top -= velocidade
                else:
                    if self.posicaoY - self.rect.top <= dist:
                        self.rect.top = self.posicaoY
                    else: self.rect.top += velocidade

        def update(self, delta):
            self.updateImage()
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
            self.textBox.rect.centery = self.rect.centery
            self.textBox.rect.left = self.iconAnimation.sprite.rect.right + int(8 * self.proporcoes.x)
            self.textBox.pos = self.textBox.rect.center

            posIcon = self.rect.center
            if self.index_sprites > 3:
                posIcon = (int(self.rect.left + 27 * self.proporcoes.x), self.rect.centery)
            self.icon.sprite.rect.center = posIcon

            rectIcone = self.icon.sprite.rect
            posIconAnimado = (rectIcone.right + int(7 * self.proporcoes.x), rectIcone.centery)
            self.iconAnimation.sprite.rect.center = posIconAnimado

            self.textBox.set_text(self.timer.get_score())
            self.mov(delta)

            if self.boxOpen:
                if self.interaction:
                    self.iconAnimation.sprite.open(delta)
                    self.textBox.enterAlpha(delta, speed=17)
                else: self.open(delta)
            else: self.close(delta)

            if self.timer.finished:
                if not self.index_sprites: self.sair = True
                self.boxOpen = False
            else:
                if self.redutivel:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.key_sprites == 'box_animation':
                        if self.rect.collidepoint(*mouse_pos):
                            self.index_sprites = 1
                            if self.audio: self.audio.reproduzir(volume=0.6)
                            if self.mouse.botaoL: self.boxOpen = True
                        else:
                            self.index_sprites = 0
                            if self.audio: self.audio.som_executado = False
                    else:
                        if self.interaction:
                            if self.rect.collidepoint(*mouse_pos):
                                self.index_sprites = self.rangeSprites - 1
                                if self.audio: self.audio.reproduzir(volume=0.6)
                                if self.mouse.botaoL:
                                    self.interaction = False
                                    self.boxOpen = False
                            else:
                                self.index_sprites = self.rangeSprites
                                if self.audio: self.audio.som_executado = False
                else: self.boxOpen = True
