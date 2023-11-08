from pygame.key import get_pressed
from pygame.transform import rotate
from Script.elementos_mapa.particulas import Particulas
from Script.objetos_abstratos.animacao import Animacao
from Script.interagiveis.bag import Bag
from Script.interagiveis.hub import Hub
from Script.gerenciadores.groups import PriorityArray
from Script.icones.life import Life
import pygame

class Player(Animacao):
    def __init__(self, sprites, proporcoes, position: tuple[int, int], priorityArray, allMessage, key_sprites="", *group) -> None:
        super().__init__(sprites, position, key_sprites, group)
        self.proporcoes = proporcoes
        self.velocidade = 0
        self.speed = 10 * self.proporcoes.x
        self.proportion_animation = 22 * self.proporcoes.x
        self.angle = 180
        self.colorPixel = None
        self.display = pygame.display.get_surface()
        self.rectDisplay = self.display.get_rect()
        self.allMessage = allMessage
        self.priorityArray = priorityArray

        self.collide = ''
        self.acaoCollide = False
        self.interaction = False
    
    def loading(self, sprites_life, mouse, clock):
        self.posMap = pygame.Vector2(int(2500 * self.proporcoes.x), int(2500 * self.proporcoes.y))
        self.particulas = Particulas(clock, priority=1, priorityArray=self.priorityArray, proporcoes=self.proporcoes)
        self.life = Life(sprites_life, clock, self.proporcoes)
        self.mouse = mouse
    
    def loadingInventory(self, spritesBag, spritesHub):
        self.allBagGroups = PriorityArray()
        self.bag = self.allBagGroups.createGroupSingle(priority=0)
        self.bag.add(Bag(spritesBag, self.proporcoes, self.allBagGroups, self.mouse, self.allMessage, self.rectDisplay.center, 'inventory_principal'))
        self.objBag = self.bag.sprite

        self.allHubGroups = PriorityArray()
        self.hub = Hub(self.objBag, spritesHub, self.allHubGroups, self.proporcoes)

    def action(self, keyboard: get_pressed, delta):
        self.velocidade = self.speed * delta
        teclas = (keyboard.key(pygame.K_a), keyboard.key(pygame.K_d),
                  keyboard.key(pygame.K_s), keyboard.key(pygame.K_w))

        if True in teclas and not self.bag.sprite.open:
            # ~~ Movimentação
            if teclas[0]:
                if not self.collide == 'a':
                    self.posMap.x -= self.velocidade
                    self.collide = ''; self.acaoCollide = False
                self.angle = 180
            elif teclas[1]:
                if not self.collide == 'd':
                    self.posMap.x += self.velocidade
                    self.collide = ''; self.acaoCollide = False
                self.angle = 0
            elif teclas[2]:
                if not self.collide == 's':
                    self.posMap.y += self.velocidade
                    self.collide = ''; self.acaoCollide = False
                self.angle = -90
            elif teclas[3]:
                if not self.collide == 'w':
                    self.posMap.y -= self.velocidade
                    self.collide = ''; self.acaoCollide = False
                self.angle = 90

            # ~~ Animação
            if not self.acaoCollide:
                if not self.collide:
                    self.key_sprites = 'caminhando'
                    self.proportion_animation = 22 * self.proporcoes.x
                    self.particulas.gerar_particula('solo', self.posMap, self.colorPixel, alcance=20)
                else:
                    self.key_sprites = 'parado'
                    self.proportion_animation = 220 * self.proporcoes.x
            else:
                self.key_sprites = 'colidindo'
                self.proportion_animation = 220 * self.proporcoes.x
        else:
            self.collide = ''; self.acaoCollide = False
            self.key_sprites = 'parado' if not self.acaoCollide else 'colidindo'
            self.proportion_animation = 220 * self.proporcoes.x if self.index_sprites < 1 or self.acaoCollide else 80 * self.proporcoes.x
        
    def update(self, mapa, keyboard, delta):
        self.rangeSprites = len(self.sprites[self.key_sprites])
        self.bag.update(delta, keyboard)
        self.life.update(self.display, delta)

        self.index_sprites += self.speed/self.proportion_animation * delta
        if self.index_sprites >= self.rangeSprites:
            if self.interaction: self.interaction = False
            self.index_sprites = 0

        self.image = self.sprites[self.key_sprites][int(self.index_sprites)]
        self.image = rotate(self.image, angle=self.angle)
        self.rect = self.image.get_rect(center=mapa.get_posRect(self.posMap))
        self.mask = pygame.mask.from_surface(self.image)

        if self.objBag.open:
            self.allBagGroups.draw(self.display)
            self.hub.update(keyboard, delta, reset=True)
        if not self.objBag.abrindo: self.hub.update(keyboard, delta)
        self.allHubGroups.draw(self.display)

        if self.interaction:
            self.key_sprites = 'interagindo'
            self.proportion_animation = 35 * self.proporcoes.x
        else: self.action(keyboard, delta)
        self.particulas.update(mapa)
