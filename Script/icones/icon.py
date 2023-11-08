import pygame, numpy

class Icon(pygame.sprite.Sprite):
    '''Icone com possibilidade de alteração de opacidade'''
    def __init__(self, sprites, pos: tuple, *groups) -> None:
        super().__init__(*groups)
        self.sumir = False
        self.index = 0
        self.indexAnt = 0
        self.array = False
        self.sprites = sprites
        if isinstance(self.sprites, numpy.ndarray):
            self.image = self.sprites[self.index]
            self.array = True
        else: self.image = self.sprites
        self.rect = self.image.get_rect(center=pos)
        self.alpha = 255
        self.speed = 20
    
    def enterAlpha(self, delta, speed=0):
        velocidade = speed * delta if speed else self.speed * delta
        if self.index != self.indexAnt:
            self.indexAnt = self.index
            self.alpha = 0

        if self.alpha < 255:
            if self.array: self.image = self.sprites[self.index].copy().convert_alpha()
            else: self.image = self.sprites.copy().convert_alpha()
            self.image.set_alpha(self.alpha)
            self.alpha += velocidade
        else: self.alpha = 255

    def closeAlpha(self, delta, speed=0):
        velocidade = speed * delta if speed else self.speed * delta
        if self.alpha > 0:
            if self.array: self.image = self.sprites[self.index].copy().convert_alpha()
            else: self.image = self.sprites.copy().convert_alpha()
            self.image.set_alpha(self.alpha)
            self.alpha -= velocidade
        else: self.sumir = True
    
    def rotate(self, angle):
        if isinstance(self.sprites, numpy.ndarray):
            for sprite in self.sprites:
                sprite = pygame.transform.rotate(sprite, angle)
            self.image = pygame.transform.rotate(self.image, angle) 
        else:
            self.sprites = pygame.transform.rotate(self.sprites, angle)
            self.image = self.sprites
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def adaptPosMap(self, pos):
        self.posMap = pygame.math.Vector2(*pos)
    
    def update(self) -> None:
        self.image = self.sprites[self.index]


class IconAnimado(Icon):
    '''Icone com animação de imagem e alteração de opacidade'''
    def __init__(self, sprites, pos: tuple, *groups) -> None:
        super().__init__(sprites, pos, *groups)
        self.index = 0
        self.speed = 1.5
    
    def open(self, delta, speed=False):
        rangeSprite = len(self.sprites)-1
        velocidade = speed * delta if speed else self.speed * delta
        self.image = self.sprites[int(self.index)]
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.index >= rangeSprite: self.index = rangeSprite
        else: self.index += velocidade
    
    def close(self, delta, speed=False):
        velocidade = speed * delta if speed else self.speed * delta
        self.image = self.sprites[int(self.index)]
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.index <= 0: self.index = 0
        else: self.index -= velocidade


class IconAnimadoTimer(Icon):
    '''Icone com animação de imagem que se repete com o tempo e alteração de opacidade'''
    def __init__(self, sprites: list, pos: tuple, timer, *groups) -> None:
        super().__init__(sprites, pos, *groups)
        self.timer = timer
        self.speed_animation = 2
    
    def update(self, delta, pausa=0) -> None:
        velocidade = self.speed_animation * delta
        self.timer.countdown(pausa)
        if self.timer.finished:
            self.index += velocidade
            if self.index >= len(self.sprites):
                self.index = 0
                self.timer.restart()
        self.image = self.sprites[int(self.index)]


class IconMoveRect(IconAnimadoTimer):
    '''Icone que se movimenta pela tela por um tempo. (Sem ancoragem no mapa)'''
    def __init__(self, sprites: list, pos: tuple, proporcoes, timer, direcao='esquerda', *groups) -> None:
        super().__init__(sprites, pos, timer, *groups)
        self.direcao = direcao
        self.proporcoes = proporcoes
        self.pos = pos[0]
        self.speed = int(1 * self.proporcoes.x)
    
    def update(self, delta, time_close=0.3):
        velocidade = self.speed * delta
        self.timer.countdown(time_close)
        if self.timer.finished:
            self.closeAlpha(delta, 30)
        match self.direcao:
            case 'esquerda': self.pos -= velocidade
            case 'direita': self.pos += velocidade
            case 'cima': self.pos -= velocidade
            case 'baixo': self.pos += velocidade

        
class IconMoveinMap(IconAnimadoTimer):
    '''Icone que se movimenta pelo mapa por um tempo. (Com anconragem no mapa)'''
    def __init__(self, sprites: list, obj_reference, proporcoes, timer, *groups) -> None:
        super().__init__(sprites, (-30, -30), timer, *groups)
        self.ref = obj_reference
        self.proporcoes = proporcoes
        distTop = self.ref.rect.centery-self.ref.rect.top+int(10 * self.proporcoes.y)
        self.posMap = pygame.math.Vector2(self.ref.posMap.x, self.ref.posMap.y-distTop)
        self.speed = int(1 * self.proporcoes.x)
    
    def update(self, delta, time_close=0.3) -> None:
        time_close *= self.proporcoes.x
        velocidade = self.speed * delta
        self.timer.countdown(time_close)
        if self.timer.finished:
            self.closeAlpha(delta, 50)
        self.posMap[1] -= velocidade
