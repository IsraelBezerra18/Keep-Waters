from Script.gerenciadores.groups import Group
from Script.objetos_abstratos.animacao import Animacao
import numpy as np

class Life:
    def __init__(self, sprites, clock, proporcoes) -> None:
        self.gameOver = False
        self.sprites = sprites
        self.proporcoes = proporcoes
        self.__valuePorcent = 0

        self.storageHeart = np.array([])
        self.hearts = Group()
        self.clock = clock
        self.loading()
    
    def loading(self):
        while self.hearts.size < 5:
            pos = (int(30 * self.proporcoes.x) + int(25 * self.proporcoes.x) * self.hearts.size, int(30 * self.proporcoes.y))
            self.storageHeart = np.append(self.storageHeart, 1)
            self.hearts.add(self.Heart(self.sprites, self.clock.createTimer(), pos))

    def queryHeart(self, condiction=1):
        listHeart = np.where(self.storageHeart == condiction)[0]
        if listHeart.size: return self.hearts.sprites()[listHeart[-1 if condiction else 0]]
        else: return False
    
    def queryIndex(self, heart):
        values = np.array(self.hearts.sprites())
        return np.where(values == heart)[0][0]
    
    def damage(self, value: int):
        self.__valuePorcent = -value
    
    def cure(self, value: int):
        self.__valuePorcent = value

    def update(self, display, delta):
        self.hearts.draw(display)
        self.hearts.update(delta)

        heartAlvo = self.queryHeart()
        if heartAlvo:
            porcent = heartAlvo.porcent
            verification = porcent + self.__valuePorcent
            if self.__valuePorcent:
                if self.__valuePorcent > 0:
                    if verification > 100:
                        heartAlvo.porcent = 100
                        newValue = verification - 100
                        newHeartAlvo = self.queryHeart(condiction=0)
                        if newHeartAlvo:
                            newHeartAlvo.porcent = newValue
                            newHeartAlvo.animationCure()
                            self.storageHeart[self.queryIndex(newHeartAlvo)] = 1
                    else:
                        heartAlvo.porcent = verification
                        heartAlvo.animationCure()
                    self.__valuePorcent = 0
                else:
                    heartAlvo.animationDamage()
                    if verification < 0:
                        heartAlvo.porcent = 0
                        self.storageHeart[self.queryIndex(heartAlvo)] = 0
                        self.__valuePorcent = verification
                    else:
                        heartAlvo.porcent = verification
                        self.__valuePorcent = 0
        else: self.gameOver = True

    class Heart(Animacao):
        def __init__(self, sprites, timer, position: tuple[int, int], key_sprites="100%", *group) -> None:
            super().__init__(sprites, position, key_sprites, *group)
            self.__porcentagem = 100
            self.action = False
            self.timer = timer
            self.speed = 0.3
        
        @property
        def porcent(self):
            return self.__porcentagem
        
        @porcent.setter
        def porcent(self, value: int):
            self.__porcentagem = value
        
        def animationCure(self):
            self.key_sprites = f'cura_{self.keyPorcent}%'
            self.index_sprites = 0
            self.action = 1

        def animationDamage(self):
            self.key_sprites = f'dano_{self.keyPorcent}%'
            self.index_sprites = 0
            self.action = -1

        def animation(self, delta):
            self.timer.contagem_regressiva(0.55)
            velocidade = self.speed * delta
            if self.index_sprites >= self.rangeSprites:
                self.index_sprites = self.rangeSprites
                if self.timer.finished: self.action = False
                else: 
                    if self.action > 0: self.key_sprites = f'cura_{self.keyPorcent}%'
                    else: self.key_sprites = f'dano_{self.keyPorcent}%'
            else:
                self.index_sprites += velocidade
                self.timer.restart()
        
        def update(self, delta):
            if self.__porcentagem > 75: self.keyPorcent = 100
            elif self.__porcentagem > 50: self.keyPorcent = 75
            elif self.__porcentagem > 25: self.keyPorcent = 50
            elif self.__porcentagem > 0: self.keyPorcent = 25
            else: self.keyPorcent = 0
            self.updateImage()

            if not self.action:
                self.key_sprites = f'{self.keyPorcent}%'
                self.index_sprites = 0
            else: self.animation(delta)
