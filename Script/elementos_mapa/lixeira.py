import pygame
from Script.objetos_abstratos.animacao import Animacao
from Script.gerenciadores.groups import Group
from Script.geometry import interactCollide

class Lixeiras:
    def __init__(self, mapa, sprites, allGroups, proporcoes) -> None:
        self.proporcoes = proporcoes
        self.sprites = sprites
        self.mapa = mapa

        self.allPerimetros = Group()
        self.groupLixeira = allGroups.createGroup(priority=1)
        self.groupPerimetro = allGroups.createGroupSingle(priority=0)
    
    def loading(self):
        self.mapa = self.mapa.sprite
        grid = self.mapa.grid
        tags, position = grid.queryObject('lixeira', 'Map')
        for tag, pos in zip(tags, position):
            verification = tag.split(' ')
            angle = 0
            if 'angle' in tag:
                angle = verification[-1]
                angle = int(angle[6:])
            tipo = verification[1]
            name = f'lixeira_{tipo}'
            lixeira = self.Lixeira(tipo, self.sprites[name], pos, grid.typeCollide(tag), angle, self.groupLixeira)
            name += '_perimetro'
            self.allPerimetros.add(self.Perimetro(self.sprites[name], lixeira, angle))
    
    def descarte(self):
        if self.groupPerimetro:
            return self.groupPerimetro.sprite
        return False

    def update(self, delta):
        self.mapa.colision(self.mapa.ref, self.groupLixeira, dist=85)
        if not self.mapa.ref.objBag.open:
            self.groupLixeira.update(self.mapa)
        self.allPerimetros.update(delta)

        colisaoPerimetro = pygame.sprite.spritecollide(self.mapa.ref, self.allPerimetros, False)
        verificacao = interactCollide(self.mapa.ref, colisaoPerimetro, int(100 * self.proporcoes.x))
        if verificacao: self.groupPerimetro.add(verificacao)
        else: self.groupPerimetro.remove(self.groupPerimetro)
        if self.groupPerimetro: self.groupPerimetro.sprite.interaction = True

    class Lixeira(pygame.sprite.Sprite):
        def __init__(self, type, sprite, posMap, colisao, angle, *groups) -> None:
            super().__init__(*groups)
            self.type = type
            self.image = sprite[0]
            if angle: self.image = pygame.transform.rotate(self.image, angle)
            self.rect = self.image.get_rect(center=(-30, -30))

            self.posMap = pygame.math.Vector2(posMap[0], posMap[1])
            self.colisao = colisao
            self.acao = False
        
        def update(self, mapa):
            self.rect = self.image.get_rect(center=mapa.get_posRect(self.posMap))
        
    class Perimetro(Animacao):
        def __init__(self, sprites, lixeira, angle, key_sprites="", *group) -> None:
            super().__init__(sprites, (-20, -20), key_sprites, *group)
            self.lixeira = lixeira
            self.interaction = False
            self.speed = 0.35
            self.type = self.lixeira.type
            if angle: self.sprites = [pygame.transform.rotate(img, angle) for img in self.sprites]
        
        def animation(self, delta):
            velocidade = self.speed * delta
            if self.index_sprites >= self.rangeSprites:
                self.index_sprites = self.rangeSprites
            else: self.index_sprites += velocidade

        def update(self, delta):
            self.rect.x = self.lixeira.rect.left
            self.rect.centery = self.lixeira.rect.centery
            self.updateImage()

            if self.interaction:
                self.animation(delta)
                self.interaction = False
            else: self.index_sprites = 0
            