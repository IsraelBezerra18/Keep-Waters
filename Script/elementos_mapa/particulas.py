import pygame, random
# from Script.geometry import get_posRect

class Particulas:
    def __init__(self, clock, priority, priorityArray, proporcoes):
        self.display = pygame.display.get_surface()
        self.particulas = priorityArray.createGroup(priority)
        self.clock = clock
        self.timer_delay = self.clock.createTimer()
        self.proporcoes = proporcoes
    
    def update(self, mapa):
        for particula in self.particulas:
            particula.vector_mov.x, particula.vector_mov.y = mapa.get_posRect(particula.pos_map)
            if particula.sumir:
                self.clock.removeTimer(particula.timer)
                self.particulas.remove(particula)
        self.particulas.update()

    def gerar_particula(self, tipo, ponto_referencia, cor, alcance,
                        delay_surgimento=0.05, dimensao=(4, 4)):
        dimensao = (int(dimensao[0] * self.proporcoes.x), int(dimensao[1] * self.proporcoes.y))
        self.timer_delay.countdown(delay_surgimento)
        if self.timer_delay.finished:
            posicao = self.sortear_pos(ponto_referencia, alcance)
            match tipo:
                case 'solo':
                    Particula_solo(posicao, dimensao, cor, self.clock.createTimer(), self.particulas)
                case 'agua':
                    pass
            self.timer_delay.restart()

    def sortear_pos(self, ponto_referencia, alcance):
        return (random.randint(int(ponto_referencia.x) - alcance, int(ponto_referencia.x) + alcance),
                random.randint(int(ponto_referencia.y) - alcance, int(ponto_referencia.y) + alcance))

class Particula_solo(pygame.sprite.Sprite):
    def __init__(self, posicao_mapa, dimensao, cor_referencia, timer, *group) -> None:
        super().__init__(group)
        self.sumir = False
        self.pos_map = pygame.math.Vector2(posicao_mapa[0], posicao_mapa[1])
        self.dimensao = dimensao
        self.new_color = pygame.Color(self.alterar_tom(cor_referencia.r), 
                                      self.alterar_tom(cor_referencia.g),
                                      self.alterar_tom(cor_referencia.b))
        self.image = pygame.Surface(self.dimensao)
        self.timer = timer
        self.vector_mov = pygame.math.Vector2()
    
    def update(self):
        self.rect = self.image.get_rect(center=self.vector_mov)
        self.timer.countdown(1)
        if self.timer.finished:
            self.sumir = True
        self.image.fill((self.new_color))
        
    @staticmethod
    def alterar_tom(tom_referencia: int, acao='soma', valor=40):
        match acao:
            case 'soma':
                return (tom_referencia + valor) if tom_referencia + valor <= 255 else 255
            case 'subtracao':
                return(tom_referencia - valor) if tom_referencia - valor >= 0 else 0
