from Script.loadFile import loadAudio
import pygame

class Audio:
    """Carrega todos os audios do diretorio especificado e armazena em um dicionário"""
    def __init__(self, diretorio) -> None:
        self.index = 0
        self.source = loadAudio(diretorio)
        self.som = pygame.sndarray.make_sound(self.source[self.index])
        self.som_executado = False
    
    def reproduzir(self, volume=1.0, repeticoes=1):
        if not self.som_executado:
            self.som.set_volume(volume)
            self.som.play(repeticoes - 1)
            self.som_executado = True
