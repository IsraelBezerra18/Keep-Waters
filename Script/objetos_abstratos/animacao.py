import pygame, numpy


# ~~ Classes abistratas
class Animacao(pygame.sprite.Sprite):
    '''O objeto abstrato Animacao é uma classe em Python que representa 
    um objeto animado para ser usado em jogos e outras aplicações de gráficos. 
    O construtor da classe carrega as imagens da animação de um diretório e 
    armazena em um dicionário. A classe define um método update, que deve ser 
    substituído nas subclasses para implementar a atualização da animação. 
    A classe Animacao é um objeto abstrato porque não pode ser instanciada 
    diretamente - uma subclasse deve ser criada para implementar a animação desejada.'''

    def __init__(self, sprites, position: tuple[int, int], key_sprites="", *group) -> None:
        super().__init__(*group)
        self.sprites = sprites
        self.key_sprites = key_sprites
        self.index_sprites = 0
        self.taxa_update = 0
        self.speed = 0
        self.image = (self.sprites[self.key_sprites][self.index_sprites] 
                if self.key_sprites else self.sprites[self.index_sprites])
        self.rect = self.image.get_rect(center=position)
        self.rangeSprites = 0
        
    def update(self) -> None:
        '''A classe define um método update, mas ele não faz nada. Esse método deve ser 
        substituído nas subclasses para implementar a atualização da animação.'''
        pass
    
    def set_posMap(self, pos: tuple):
        self.posMap.x = pos[0]
        self.posMap.y = pos[1]
    
    def draw(self, display):
        display.blit(self.image, self.rect.center)

    def updateImage(self):
        if 0 <= self.index_sprites <= self.rangeSprites:
            if self.key_sprites:
                self.image = self.sprites[self.key_sprites][int(self.index_sprites)]
            else: self.image = self.sprites[int(self.index_sprites)]
            self.rangeSprites = self.get_sizeKey()

    def get_sizeKey(self, key=''):
        if isinstance(self.sprites, numpy.ndarray):
            return len(self.sprites)-1
        if key: return len(self.sprites[key])-1
        return len(self.sprites[self.key_sprites])-1
