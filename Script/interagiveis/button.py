import pygame
from Script.reprodutores.audio import Audio
from Script.objetos_abstratos.animacao import Animacao

class Botao(Animacao):
    def __init__(self, sprites, audio:Audio, position: tuple[int,int], 
                 key_sprites: str, text: str, textManager, sizeText=40):
        super().__init__(sprites, position, key_sprites=key_sprites)
        self.estado = False
        self.audio = audio
        self.textManager = textManager
        self.mask = pygame.mask.from_surface(self.image)
        self.padrao = ""
        self.id = text
        self.velocidade_padrao = 0.2

        # ~~ Texto do botão
        self.size_text = sizeText
        self.texto = self.textManager.createText(text, self.size_text, self.rect.center)
        if text: self.textManager.ajustsize(self)

    def execute(self, delta):
        velocidade = self.velocidade_padrao * delta
        self.key_sprites = (self.key_sprites + self.padrao if self.padrao not in self.key_sprites else self.key_sprites)
        self.updateImage()
            
        if 'interface' in self.key_sprites:
            proporcao = 10
            self.index_sprites += (velocidade/proporcao if self.index_sprites < 1 or 
            self.index_sprites >= self.rangeSprites - 1.1 else velocidade)
            if self.index_sprites >= self.rangeSprites - 0.1 or self.index_sprites <= 0:
                self.velocidade_padrao = -self.velocidade_padrao
        elif 'acao' in self.key_sprites:
            self.index_sprites += velocidade
            if self.index_sprites > self.rangeSprites - 1:
                self.index_sprites = self.rangeSprites - 1
        else: self.index_sprites = 1

        if self.audio: self.audio.reproduzir(volume=0.6)
    
    def reset(self):
        self.key_sprites = self.key_sprites.replace(self.padrao, "")
        self.image = self.sprites[self.key_sprites][0]
        self.index_sprites = 0
        self.velocidade_padrao = 0.2
        if self.audio: self.audio.som_executado = False

    def update(self, tela, delta, padrao_colide, condition: bool):
        mouse_pos = pygame.mouse.get_pos()
        mask_mouse = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
        self.padrao = padrao_colide

        if self.rect.collidepoint(*mouse_pos) and self.mask.get_at(mask_mouse):
            self.execute(delta)
        else: self.reset()

        if condition and self.rect.collidepoint(*mouse_pos):
            self.estado = True
        else: self.estado = False

class BotaoIcon(Botao):
    def __init__(self, sprites, audio: Audio, position: tuple[int, int], textManager, text='', key_sprites='', sizeText=40):
        super().__init__(sprites, audio, position, key_sprites, text, textManager, sizeText)
        self.alpha = 0
        self.speed = 20
        self.interaction = False

        self.reference = self.image
        self.image = self.reference.copy()
        self.image.set_alpha(self.alpha)
        self.texto.set_alpha(0)
        self.rangeSprites = self.get_sizeKey()

    def execute(self):
        if self.audio: self.audio.reproduzir(volume=0.6)
        self.index_sprites = 1

    def reset(self):
        if self.audio: self.audio.som_executado = False
        self.index_sprites = 0
    
    def ajustAparence(self):
        if self.key_sprites:
            self.reference = self.sprites[self.key_sprites][int(self.index_sprites)]
        else: self.reference = self.sprites[int(self.index_sprites)]
        self.image = self.reference.copy().convert_alpha()
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def set_alpha(self, value: int):
        self.alpha = value; self.ajustAparence()
        
    def enterAlpha(self, delta, speed=False):
        if self.alpha < 255:
            self.ajustAparence()
            self.alpha += speed * delta if speed else self.speed * delta
        else: self.alpha = 255
    
    def closeAlpha(self, delta, speed=False):
        if self.alpha < 0:
            self.ajustAparence()
            self.alpha -= speed * delta if speed else self.speed * delta
        else: self.alpha = 0
    
    def enter(self, keyDest, speed, delta):
        velocidade = speed * delta
        self.ajustAparence()

        if self.index_sprites >= self.rangeSprites:
            self.index_sprites = self.rangeSprites
            if self.key_sprites != keyDest:
                self.key_sprites = keyDest
                self.index_sprites = 0
                self.interaction = True
                self.mask = pygame.mask.from_surface(self.sprites[self.key_sprites][-1])
        else: self.index_sprites += velocidade
        
    def close(self, keyDest, speed, delta):
        self.interaction = False
        velocidade = speed * delta
        self.ajustAparence()

        if self.index_sprites <= 0:
            self.index_sprites = 0
            if self.key_sprites != keyDest:
                self.key_sprites = keyDest
                self.index_sprites = self.get_sizeKey(keyDest)
        else: self.index_sprites -= velocidade

    def update(self, delta, mouse):
        self.estado = False
        self.ajustAparence()
        mouse_pos = pygame.mouse.get_pos()
        mask_mouse = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y

        if self.rect.collidepoint(*mouse_pos) and self.mask.get_at(mask_mouse):
            self.execute()
            if mouse.botaoL: self.estado = True
        else: self.reset()
        if self.estado: self.execute()

# ~~ Botões do Player de Vídeo ~~ #

class BotaoFrame(Botao):
    def __init__(self, sprites, audio: Audio, position: tuple[int, int], key_sprites='', text='', color_text=(202, 218, 234)):
        super().__init__(sprites, audio, position, key_sprites, text, color_text)
        self.reproduzido = False

    def update(self, condition: bool, indexFrame):
        mouse_pos = pygame.mouse.get_pos()
        if self.id > indexFrame:
            self.reproduzido = False
        if self.id < indexFrame:
            self.reproduzido = True

        if self.rect.collidepoint(*mouse_pos):
            if self.reproduzido: self.index_sprites = 0
            else: self.index_sprites = 1
            if condition: self.estado = True
            else: self.estado = False
        else:
            self.index_sprites = 0
            self.estado = False
            if self.reproduzido: self.index_sprites = 1
        self.image = self.sprites[self.index_sprites]

class BotaoAtivar(BotaoIcon):
    def __init__(self, sprites, audio: Audio, position: tuple[int, int]):
        super().__init__(sprites, audio, position)

    def update(self, condition: bool):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*mouse_pos):
            if self.estado: self.execute()
            else: self.reset()
            if condition: self.estado = False if self.estado else True
        if self.estado: self.execute()
        self.image = self.sprites[self.index_sprites]
