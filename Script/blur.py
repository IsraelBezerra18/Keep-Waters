from PIL import Image, ImageFilter
from Script.gerenciadores.groups import GroupSingle
import pygame, numpy as np

class Blur:
    def __init__(self, display) -> None:
        self.display = display
        self.image = GroupSingle()
        self.active = False

    @property
    def unfocused(self):
        if self.image:
            blur = self.image.sprite
            if blur.unfocused: return True
        return False

    def createImage(self, reference, desfoque):
        size = reference.get_size()
        imagem = pygame.image.tostring(reference, 'RGBA')
        imagemPil = Image.frombytes('RGBA', size, imagem)
        image = imagemPil.filter(desfoque)
        return pygame.image.fromstring(image.tobytes(), size, 'RGBA').convert_alpha()

    def create(self, condiction, surface, desfoque: int):
        if condiction:
            reference = surface.copy().convert_alpha()
            listDesfoque = np.array([ImageFilter.GaussianBlur(i) for i in range(desfoque + 1)])
            sprites = np.array([self.createImage(reference, desfoque) for desfoque in listDesfoque])
            self.image.add(self.Image(sprites))
    
    def apply(self):
        self.active = True

    def remove(self):
        if self.image: self.image.sprite.sair = True
    
    def update(self, delta):
        if self.image:
            blur = self.image.sprite
            self.image.update(self.active, delta)
            if blur.image: self.image.draw(self.display)

            if blur.sair and not blur.desfoque:
                self.image.remove(self.image)
                self.active = False
    
    class Image(pygame.sprite.Sprite):
        def __init__(self, sprites, *groups) -> None:
            super().__init__(*groups)
            self.unfocused = False
            self.sair = False
            self.image = None

            self.sprites = sprites
            self.rangeSprites = len(self.sprites)-1
            self.rect = self.sprites[0].get_rect()
            self.desfoque = 0
            self.speed = 0.25

        def update(self, condiction, delta):
            velocidade = self.speed * delta
            self.image = self.sprites[int(self.desfoque)]

            if condiction:
                if self.sair:
                    self.unfocused = False
                    if self.desfoque <= 0:
                        self.desfoque = 0
                        self.unfocused = True
                    else: self.desfoque -= velocidade
                else:
                    if self.desfoque >= self.rangeSprites:
                        self.desfoque = self.rangeSprites
                        self.unfocused = True
                    else: self.desfoque += velocidade
