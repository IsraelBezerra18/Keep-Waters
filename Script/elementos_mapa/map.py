from Script.grid import Grid
from Script.geometry import getDist
from Script.geometry import get_posImage, get_posRect, get_colorPixel, interactCollide
from Script.loadFile import resize
import pygame

proporcao = 4
image_mapa = 'Data/Imagens/mapas/mapa_principal.png'
arquivo_exel = "Data/Exel/mapa.xlsx"

class Map(pygame.sprite.Sprite):
    def __init__(self, player, display, proporcoes, *group) -> None:
        super().__init__(*group)
        self.display = display
        self.rect_display = display.get_rect()
        self.proporcoes = proporcoes
        self.ref = player

        self.image = pygame.image.load(image_mapa)
        self.width, self.height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (self.width*proporcao, self.height*proporcao))
        self.image = resize(self.image, self.proporcoes)

        self.rect = self.image.get_rect()
        self.grid = Grid(self.proporcoes, self.display, arquivo_exel)
        self.grid.set_distance(distance=50)

    def loading(self):
        self.grid.invibleBarrier((35, 35))

    def update(self) -> None:
        self.grid.update(self)
        self.rect.x = -self.ref.posMap.x + int(640 * self.proporcoes.x)
        self.rect.y = -self.ref.posMap.y + int(360 * self.proporcoes.y)
        self.ref.colorPixel = self.get_colorPixel(self.ref.posMap)

        # ~~ Condições de movimento do eixo X
        if self.rect.left >= 0:
            self.rect.left = 0

        elif self.rect.right <= self.rect_display.width:
            self.rect.right = self.rect_display.width

        # ~~ Condições de movimento do eixo Y
        if self.rect.top >= 0:
            self.rect.top = 0
            
        elif self.rect.bottom <= self.rect_display.height:
            self.rect.bottom = self.rect_display.height

    def get_posRect(self, vector):
        '''Retorna a posição do vetor na tela com relação ao mapa.'''
        if not isinstance(vector, pygame.Vector2):
            vector = pygame.Vector2(*vector)
        return get_posRect(self, vector)

    def get_posMap(self, rect):
        '''Retorna onde o rect está no mapa.'''
        return get_posImage(self, (rect.centerx, rect.centery))

    def get_colorPixel(self, vector):
        '''Retorna a cor do pixel na posição relativa ao mapa.'''
        return get_colorPixel(self, vector)

    def colision(self, sprite, grupo, dist=100):
        '''Realiza a colisão física entre um objeto referência e um grupo de objetos.'''
        colisao = False; dist *= self.proporcoes.x
        if not self.ref.objBag.open:
            colisao = pygame.sprite.spritecollide(sprite, grupo, False)
            colisao = interactCollide(sprite, colisao, dist)

        def verificacao_h():
            if cr and dist_lr < 45 * self.proporcoes.x:
                sprite.posMap.x += sprite.velocidade
                return False
            elif cl and dist_rl < 45 * self.proporcoes.x:
                sprite.posMap.x -= sprite.velocidade
                return False
            return True
            
        def verificacao_v():
            if ct and dist_bt < 45 * self.proporcoes.y:
                sprite.posMap.y -= sprite.velocidade
                return False
            elif cb and dist_tb < (45 * self.proporcoes.y):
                sprite.posMap.y += sprite.velocidade
                return False
            return True

        if colisao:
            ct, cb, cl, cr = colisao.colisao
            dist_rl = getDist((sprite.rect.right, 0), (colisao.rect.left, 0))
            dist_lr = getDist((sprite.rect.left, 0), (colisao.rect.right, 0))
            dist_tb = getDist((0, sprite.rect.top), (0, colisao.rect.bottom))
            dist_bt = getDist((0, sprite.rect.bottom), (0, colisao.rect.top))

            if ct and verificacao_h():
                if sprite.rect.centery < colisao.rect.centery:
                    sprite.rect.bottom = colisao.rect.top
                    sprite.posMap.x, sprite.posMap.y = self.get_posMap(sprite.rect)
                    sprite.collide = 's'
            if cb and verificacao_h():
                if sprite.rect.centery > colisao.rect.centery:
                    sprite.rect.top = colisao.rect.bottom
                    sprite.posMap.x, sprite.posMap.y = self.get_posMap(sprite.rect)
                    sprite.collide = 'w'
            
            if cl and verificacao_v():
                if sprite.rect.centerx < colisao.rect.centerx:
                    sprite.rect.right = colisao.rect.left
                    sprite.posMap.x, sprite.posMap.y = self.get_posMap(sprite.rect)
                    sprite.collide = 'd'
            if cr and verificacao_v():
                if sprite.rect.centerx > colisao.rect.centerx:
                    sprite.rect.left = colisao.rect.right
                    sprite.posMap.x, sprite.posMap.y = self.get_posMap(sprite.rect)
                    sprite.collide = 'a'
            sprite.acaoCollide = colisao.acao
