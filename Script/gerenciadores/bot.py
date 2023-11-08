import pygame
from Script.geometry import getDist

class Bot:
    def __init__(self, pos):
        self.speed = 2
        self.posMap = pygame.Vector2(*pos)
        self.posCurrent = self.posMap.xy
        self.current = None
        self.listPath = None
    
    def set_path(self, path):
        if path:
            if self.listPath != path:
                self.listPath = path
                self.current = self.listPath.pop(0)
        else: self.current = None
    
    def move(self, delta):
        if self.current:
            velocidade = self.speed * delta

            dx = self.posCurrent[0] - self.posMap.x
            dy = self.posCurrent[1] - self.posMap.y
            
            if abs(dx) != abs(dy):
                if abs(dx) > abs(dy): dy = 0
                else: dx = 0

            dist = abs(dx) + abs(dy)
            if dist > 1:
                dx /= dist
                dy /= dist

                movX = dx * velocidade
                movY = dy * velocidade
                self.posMap.x += movX
                self.posMap.y += movY
            else:
                self.current = self.listPath.pop(0) if self.listPath else None
                if self.current: self.posCurrent = self.current.posMap.xy

    def draw(self, display, mapa):
        pygame.draw.circle(display, (0, 0, 255), mapa.get_posRect(self.posMap), 15)
