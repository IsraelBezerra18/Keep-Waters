import pygame

class Keyboard:
    def __init__(self) -> None:
        self.evento = None

    def key(self, tecla):
        self.teclas = pygame.key.get_pressed()
        return self.teclas[tecla]

    def event(self, tecla):
        if self.evento == tecla:
            return True
        return False
    
    def getkey(self):
        if self.evento: return pygame.key.name(self.evento)
