import pygame, numpy as np
from Script.objetos_abstratos.interface import Interface
from Script.reprodutores.audio import Audio
from Script.interagiveis.button import Botao
from Script.gerenciadores.text import TextManager
from Script.objetos_abstratos.animacao import Animacao
from Script.loadFile import loadImage

menu_inicial = 'Data/Imagens/interfaces/menus_principais/menu_inicial/'
botao_interface = 'Data/Imagens/botoes/botao_interface/'
audio = 'Data/Audios/sons_botao/interface/'

class PrincipalInterface(Interface):
    def __init__(self, map_list, size_block, ArrayGroup, proporcoes) -> None:
        super().__init__(map_list)
        self.init = True
        self.display = pygame.display.get_surface()
        self.proporcoes = proporcoes
        self.sizeBlockX = int(size_block * self.proporcoes.x)
        self.sizeBlockY = int(size_block * self.proporcoes.y)

        # ~~ Gerenciadores
        self.allText = TextManager(self.proporcoes)

        # ~~ Grupos
        self.allGroup = ArrayGroup
        self.background = self.allGroup.createGroupSingle(priority=0)
        self.buttons = self.allGroup.createGroup(priority=5)
    
    def loading(self, list_of_objects: list[str]):
        self.background.add(self.Background(loadImage(menu_inicial, self.proporcoes, type='list', argumento=(1280, 720), 
                            transform=pygame.transform.scale), position=self.display.get_rect().center))
        
        button_interface = loadImage(botao_interface, self.proporcoes, argumento=(350, 65), transform=pygame.transform.scale)
        for key in list_of_objects:
            y, x = np.where(self.map == key)
            self.buttons.add(Botao(button_interface, audio=Audio(audio), position=(x*self.sizeBlockX, y*self.sizeBlockY), 
                                   key_sprites='botao_interface', text=key, textManager=self.allText, sizeText=30))
    
    def inputs(self, key):
        match key:
            case 'Jogar', True:
                self.init = False
            case 'Sair do jogo', True:
                return False
            
    def run(self, mouse, delta):
        if self.init:
            self.allGroup.draw(self.display)
            self.allText.blit(self.display)
            
            self.background.update(delta)
            self.buttons.update(self.display, delta, '_colide', mouse.botaoL)

    class Background(Animacao):
        def __init__(self, sprites, position: tuple[int, int], key_sprites="", *group) -> None:
            super().__init__(sprites, position, key_sprites, *group)
            self.taxa_update = 0.08
        
        def update(self, delta) -> None:
            velocidade = self.taxa_update * delta
            if self.index_sprites >= len(self.sprites):
                self.index_sprites = 0
            self.image = self.sprites[int(self.index_sprites)]
            self.index_sprites += velocidade
    